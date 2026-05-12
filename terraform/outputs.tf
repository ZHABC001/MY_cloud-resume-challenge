
output "s3_bucket_name" {
  description = "S3 バケット名"
  value       = aws_s3_bucket.resume.id
}

output "s3_website_endpoint" {
  description = "S3 静的ウェブサイトの URL"
  value       = aws_s3_bucket_website_configuration.resume.website_endpoint
}

output "s3_bucket_arn" {
  description = "S3 バケットの ARN"
  value       = aws_s3_bucket.resume.arn
}

output "dynamodb_table_name" {
  description = "DynamoDB テーブル名"
  value       = aws_dynamodb_table.visitor_counter.name
}

output "lambda_function_name" {
  description = "Lambda 関数名"
  value       = aws_lambda_function.resume_counter.function_name
}

output "lambda_function_arn" {
  description = "Lambda 関数の ARN"
  value       = aws_lambda_function.resume_counter.arn
}

output "iam_role_arn" {
  description = "Lambda 実行ロールの ARN"
  value       = aws_iam_role.lambda_resume_counter.arn
}

output "dynamodb_table_arn" {
  description = "DynamoDB テーブルの ARN"
  value       = aws_dynamodb_table.visitor_counter.arn
}

output "api_gateway_id" {
  description = "API Gateway ID"
  value       = aws_apigatewayv2_api.counter_api.id
}

output "api_gateway_endpoint" {
  description = "API Gateway のエンドポイント URL"
  value       = aws_apigatewayv2_api.counter_api.api_endpoint
}

output "api_gateway_invoke_url" {
  description = "訪問者カウンター API の完全な URL"
  value       = "${aws_apigatewayv2_api.counter_api.api_endpoint}/counter"
}