import json


def lambda_handler(event, context):
    headers = {
        "Access-Control-Allow-Origin": "https://zhabc001.me",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "POST,OPTIONS",
        "Content-Type": "application/json"
    }

    method = event.get("requestContext", {}).get("http", {}).get("method")

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
                "body": json.dumps({"error": "Question is required"})
            }

        if len(question) > 500:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({"error": "Question is too long"})
            }

        answer = (
            "This is a test response from the AI Assistant Lambda. "
            "In the next version, this API will call an LLM API securely from the backend."
        )

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
            "body": json.dumps({"error": "Internal server error"})
        }