resource "aws_dynamodb_table" "ai_assistant_logs" {
  name         = "ai_assistant_logs"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "request_id"

  attribute {
    name = "request_id"
    type = "S"
  }

  ttl {
    attribute_name = "expires_at"
    enabled        = true
  }

  tags = {
    Name = "ai_assistant_logs"
  }
}

data "archive_file" "ai_assistant_zip" {
  type        = "zip"
  source_file = "${path.module}/../backend/ai_assistant/lambda_function.py"
  output_path = "${path.module}/ai_assistant_lambda.zip"
}

data "aws_iam_policy_document" "ai_assistant_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "ai_assistant_lambda_role" {
  name               = "ai-assistant-lambda-role"
  assume_role_policy = data.aws_iam_policy_document.ai_assistant_assume_role.json
}

data "aws_iam_policy_document" "ai_assistant_lambda_policy_doc" {
  statement {
    sid = "AllowCloudWatchLogs"

    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]

    resources = [
      "${aws_cloudwatch_log_group.ai_assistant.arn}:*"
    ]
  }

  statement {
    sid = "AllowPutItemToAiAssistantLogs"

    actions = [
      "dynamodb:PutItem"
    ]

    resources = [
      aws_dynamodb_table.ai_assistant_logs.arn
    ]
  }
}

resource "aws_iam_policy" "ai_assistant_lambda_policy" {
  name   = "ai-assistant-lambda-policy"
  policy = data.aws_iam_policy_document.ai_assistant_lambda_policy_doc.json
}

resource "aws_iam_role_policy_attachment" "ai_assistant_lambda_policy_attachment" {
  role       = aws_iam_role.ai_assistant_lambda_role.name
  policy_arn = aws_iam_policy.ai_assistant_lambda_policy.arn
}

resource "aws_cloudwatch_log_group" "ai_assistant" {
  name              = "/aws/lambda/ai-assistant-api"
  retention_in_days = 30
}

resource "aws_apigatewayv2_integration" "ai_assistant" {
  api_id                 = aws_apigatewayv2_api.counter_api.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.ai_assistant.invoke_arn
  integration_method     = "POST"
  payload_format_version = "2.0"
}

output "ai_assistant_lambda_name" {
  value = aws_lambda_function.ai_assistant.function_name
}

output "ai_assistant_logs_table_name" {
  value = aws_dynamodb_table.ai_assistant_logs.name
}

resource "aws_lambda_function" "ai_assistant" {
  function_name = "ai-assistant-api"
  role          = aws_iam_role.ai_assistant_lambda_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.12"

  filename         = data.archive_file.ai_assistant_zip.output_path
  source_code_hash = data.archive_file.ai_assistant_zip.output_base64sha256

  timeout     = 30
  memory_size = 256

  environment {
    variables = {
      LOG_TABLE_NAME  = aws_dynamodb_table.ai_assistant_logs.name
      GEMINI_API_KEY  = var.gemini_api_key
      IP_HASH_SALT    = var.ip_hash_salt
      ALLOWED_ORIGINS = join(",", var.allowed_origins)
    }
  }

  depends_on = [
    aws_cloudwatch_log_group.ai_assistant,
    aws_iam_role_policy_attachment.ai_assistant_lambda_policy_attachment
  ]
}

resource "aws_apigatewayv2_route" "ask" {
  api_id    = aws_apigatewayv2_api.counter_api.id
  route_key = "POST /ask"
  target    = "integrations/${aws_apigatewayv2_integration.ai_assistant.id}"
}

resource "aws_lambda_permission" "allow_api_gateway_ai_assistant" {
  statement_id  = "AllowExecutionFromAPIGatewayAiAssistant"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ai_assistant.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.counter_api.execution_arn}/*/*"
}