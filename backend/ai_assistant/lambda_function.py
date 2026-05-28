import json
import os
import urllib.request
import urllib.error

ALLOWED_ORIGINS = {
    "https://zhabc001.me",
    "http://localhost:63342",
    "http://127.0.0.1:5500"
}

GEMINI_MODEL = "gemini-2.5-flash-lite"

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


def build_headers(event):
    headers_from_request = event.get("headers") or {}
    origin = headers_from_request.get("origin") or headers_from_request.get("Origin")

    allow_origin = origin if origin in ALLOWED_ORIGINS else "https://zhabc001.me"

    return {
        "Access-Control-Allow-Origin": allow_origin,
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "POST,OPTIONS",
        "Content-Type": "application/json"
    }


def lambda_handler(event, context):
    headers = build_headers(event)

    method = (
        event.get("requestContext", {})
        .get("http", {})
        .get("method")
    )

    if method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({"message": "ok"})
        }

    try:
        body = json.loads(event.get("body") or "{}")
        question = body.get("question", "").strip()

        if not question:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({"error": "Question is required"}, ensure_ascii=False)
            }

        if len(question) > 500:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({"error": "Question is too long"}, ensure_ascii=False)
            }

        answer = call_gemini(question)

        return {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps({"answer": answer}, ensure_ascii=False)
        }

    except Exception as e:
        print("Error:", str(e))

        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps(
                {"error": "Internal server error"},
                ensure_ascii=False
            )
        }


def call_gemini(question):
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set")

    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{GEMINI_MODEL}:generateContent?key={api_key}"
    )

    prompt = f"""
{PROJECT_CONTEXT}

The following user question is asked on Zhang Beichuan's portfolio website.
Interpret "this project", "このプロジェクト", and "这个项目" as the Cloud Resume Challenge portfolio project.

User question:
{question}

Please answer directly without refusing if the question is about this portfolio project.

Answer:
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
            "maxOutputTokens": 700
        }
    }
