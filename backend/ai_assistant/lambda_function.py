import json
import os
import time
import uuid
import hashlib
import urllib.request
import urllib.error
from datetime import datetime
from zoneinfo import ZoneInfo

import boto3


# =========================
# Environment variables
# =========================

GEMINI_MODEL = "gemini-2.5-flash-lite"

LOG_TABLE_NAME = os.environ.get("LOG_TABLE_NAME", "ai_assistant_logs")
IP_HASH_SALT = os.environ.get("IP_HASH_SALT", "")

dynamodb = boto3.resource("dynamodb", region_name="ap-northeast-1")
log_table = dynamodb.Table(LOG_TABLE_NAME)


def load_allowed_origins():
    """ALLOWED_ORIGINSを環境変数から読み込む"""
    env_value = os.environ.get("ALLOWED_ORIGINS", "")

    if env_value:
        return {
            origin.strip()
            for origin in env_value.split(",")
            if origin.strip()
        }

    return {
        "https://zhabc001.me",
        "http://localhost:63342",
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    }


ALLOWED_ORIGINS = load_allowed_origins()


PROJECT_CONTEXT = """
You are an AI assistant embedded in Zhang Beichuan's portfolio website.

Your main purpose:
Explain Zhang Beichuan's Cloud Resume Challenge project, AWS architecture,
technical skills, research background, and interview preparation points.

Very important:
When the user says "this project", "このプロジェクト", "このサイト", "このポートフォリオ",
"这个项目", or "这个网站", they are referring to Zhang Beichuan's Cloud Resume Challenge portfolio project.
Do not reject these questions as unrelated.

Answer rules:
- If the question is about the portfolio, Cloud Resume Challenge, AWS architecture,
  technical skills, career preparation, interview preparation, or Zhang Beichuan's background, answer it.
- If the question is clearly unrelated, politely say that you can only answer questions about this portfolio project.
- Keep answers concise and practical.
- If the user asks in Japanese, answer in Japanese.
- If the user asks in English, answer in English.
- If the user asks in Chinese, answer in Chinese.

Portfolio information:
- Name: Zhang Beichuan / 張 北川
- 2027 master's student at Chiba Institute of Technology.
- Target career: cloud engineer, infrastructure engineer, SRE, or cloud-related IT role.
- Certifications: AWS Certified Solutions Architect - Associate, JLPT N2, TOEIC 840.
- Cloud Resume Challenge project:
  - Static resume website
  - AWS Lambda backend
  - API Gateway
  - DynamoDB visitor counter
  - CloudWatch monitoring
  - GitHub Actions CI/CD
  - Terraform for infrastructure as code
  - S3 / CDN-based website hosting
- Project focus:
  - Serverless architecture
  - Cost optimization
  - Observability
  - Security awareness
  - Not exposing API keys in frontend code
- AI Assistant feature:
  - Frontend calls API Gateway
  - API Gateway invokes Lambda
  - Lambda securely calls Gemini API
  - Gemini API key is stored in Lambda environment variables
  - The frontend does not expose API keys
- Research topic:
  - Moving Target Defense strategy in multi-cloud environments using game theory.
  - Focus on security-cost trade-offs in multi-cloud environments.
"""


# =========================
# Common helpers
# =========================

def build_headers(event):
    headers_from_request = event.get("headers") or {}
    origin = (
        headers_from_request.get("origin")
        or headers_from_request.get("Origin")
    )

    allow_origin = origin if origin in ALLOWED_ORIGINS else "https://zhabc001.me"

    return {
        "Access-Control-Allow-Origin": allow_origin,
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "POST,OPTIONS",
        "Content-Type": "application/json"
    }


def get_client_ip(event):
    """API Gateway eventからIPアドレスを取得する"""
    return (
        event.get("requestContext", {})
        .get("http", {})
        .get("sourceIp", "unknown")
    )


def get_user_agent(event):
    """User-Agentを取得する"""
    headers = event.get("headers") or {}

    return (
        headers.get("user-agent")
        or headers.get("User-Agent")
        or "unknown"
    )


def hash_ip(ip_address):
    """IPアドレスをそのまま保存せず、salt付きでハッシュ化する"""
    raw = f"{ip_address}:{IP_HASH_SALT}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def save_request_log(event, question, status):
    """AI AssistantのリクエストメタデータをDynamoDBに保存する"""
    now = int(time.time())
    ttl_days = 30

    tokyo_time = datetime.fromtimestamp(now, ZoneInfo("Asia/Tokyo"))

    client_ip = get_client_ip(event)
    ip_hash = hash_ip(client_ip)
    user_agent = get_user_agent(event)

    item = {
        "request_id": str(uuid.uuid4()),
        "created_at": now,
        "created_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now)),
        "created_at_jst": tokyo_time.strftime("%Y-%m-%d %H:%M:%S JST"),
        "expires_at": now + ttl_days * 24 * 60 * 60,
        "ip_hash": ip_hash,
        "user_agent": user_agent[:300],
        "question_length": len(question) if question else 0,
        "status": status
    }

    log_table.put_item(Item=item)


def safe_save_request_log(event, question, status):
    """ログ保存に失敗しても、AI回答自体は止めない"""
    try:
        save_request_log(event, question, status)
    except Exception as log_error:
        print("Log save error:", str(log_error))


# =========================
# Lambda handler
# =========================

def lambda_handler(event, context):
    headers = build_headers(event)

    method = (
        event.get("requestContext", {})
        .get("http", {})
        .get("method")
    )

    print("AI Assistant Lambda invoked")
    print("event keys:", list(event.keys()))

    if method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({"message": "ok"}, ensure_ascii=False)
        }

    question = ""

    try:
        raw_body = event.get("body") or "{}"
        print("body length:", len(raw_body))

        body = json.loads(raw_body)
        question = body.get("question", "").strip()

        print("question length:", len(question))

        if not question:
            safe_save_request_log(event, question, "error_empty_question")
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps(
                    {"error": "Question is required"},
                    ensure_ascii=False
                )
            }

        if len(question) > 500:
            safe_save_request_log(event, question, "error_question_too_long")
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps(
                    {"error": "Question is too long"},
                    ensure_ascii=False
                )
            }

        answer = call_gemini(question)
        print("answer length:", len(answer) if answer else 0)

        if not answer:
            print("Empty answer from Gemini")
            safe_save_request_log(event, question, "error_empty_answer")
            return {
                "statusCode": 502,
                "headers": headers,
                "body": json.dumps(
                    {"error": "AI response was empty"},
                    ensure_ascii=False
                )
            }

        safe_save_request_log(event, question, "success")

        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps(
                {"answer": answer},
                ensure_ascii=False
            )
        }

    except json.JSONDecodeError as e:
        print("JSON decode error:", str(e))
        safe_save_request_log(event, question, "error_invalid_json")

        return {
            "statusCode": 400,
            "headers": headers,
            "body": json.dumps(
                {"error": "Invalid JSON"},
                ensure_ascii=False
            )
        }

    except Exception as e:
        import traceback
        print("Error:", str(e))
        print(traceback.format_exc())

        safe_save_request_log(event, question, "error")

        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps(
                {"error": "Internal server error"},
                ensure_ascii=False
            )
        }


# =========================
# Gemini API
# =========================

def call_gemini(question):
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set")

    print("call_gemini started")
    print("gemini api key exists:", bool(api_key))

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{GEMINI_MODEL}:generateContent?key={api_key}"
    )

    prompt = f"""
{PROJECT_CONTEXT}

あなたは張北川のポートフォリオサイトに設置されたAI Assistantです。
以下の質問に対して、ポートフォリオ、AWS構成、使用技術、面接説明に関係する範囲で答えてください。
分からないことは推測せず、「分かりません」と答えてください。

質問:
{question}
"""

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 512
        }
    }

    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            response_body = response.read().decode("utf-8")

        print("gemini response received")

        response_json = json.loads(response_body)

        candidates = response_json.get("candidates", [])

        if not candidates:
            print("Gemini response has no candidates:", response_body[:500])
            return ""

        answer = (
            candidates[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "")
        )

        return answer.strip()

    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print("Gemini HTTPError:", e.code, error_body)
        raise

    except urllib.error.URLError as e:
        print("Gemini URLError:", str(e))
        raise
