# 文件: terraform/main.tf

# ===========================================
# Terraform & Provider 設定
# ===========================================

terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  # すべてのリソースに自動付与されるデフォルトタグ
  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      Owner       = var.owner
      ManagedBy   = "Terraform"
    }
  }
}

# ===========================================
# S3 Bucket: 履歴書サイトの静的ホスティング
# ===========================================

# Bucket 本体
resource "aws_s3_bucket" "resume" {
  bucket = var.s3_bucket_name
}

# 静的ウェブサイトホスティング設定
resource "aws_s3_bucket_website_configuration" "resume" {
  bucket = aws_s3_bucket.resume.id

  index_document {
    suffix = "ZHANG_BEICHUAN_Cloud_Resume.html"
  }

  error_document {
    key = "ZHANG_BEICHUAN_Cloud_Resume.html"
  }
}

# パブリックアクセス設定 (応急版用)
resource "aws_s3_bucket_public_access_block" "resume" {
  bucket = aws_s3_bucket.resume.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

# パブリック読み取り権限のバケットポリシー
resource "aws_s3_bucket_policy" "resume_public_read" {
  bucket = aws_s3_bucket.resume.id

  depends_on = [aws_s3_bucket_public_access_block.resume]

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.resume.arn}/*"
      }
    ]
  })
}

# ===========================================
# DynamoDB Table: 訪問者カウンター
# ===========================================

resource "aws_dynamodb_table" "visitor_counter" {
  name         = var.dynamodb_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }

  # ポイントインタイムリカバリ (PITR) - 推奨
  point_in_time_recovery {
    enabled = false  # 応急版では無効、本番では有効化推奨
  }

  # 削除保護 - SRE ベストプラクティス
  deletion_protection_enabled = false  # 開発フェーズでは false、本番では true
}

# ===========================================
# Lambda Function: 訪問者カウンター
# ===========================================

# Lambda 関数のコードを zip にパッケージング
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/../backend/lambda/lambda_function.py"
  output_path = "${path.module}/lambda_function.zip"
}

# IAM Role: Lambda 実行ロール
resource "aws_iam_role" "lambda_resume_counter" {
  name = "lambda-resume-counter-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# IAM Policy: DynamoDB 最小権限ポリシー
resource "aws_iam_policy" "lambda_dynamodb_counter" {
  name        = "LambdaResumeCounterDynamoDBPolicy"
  description = "Lambda 用の DynamoDB 最小権限ポリシー"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowUpdateCounter"
        Effect = "Allow"
        Action = [
          "dynamodb:UpdateItem"
        ]
        Resource = aws_dynamodb_table.visitor_counter.arn
      }
    ]
  })
}

# Attach DynamoDB policy to role
resource "aws_iam_role_policy_attachment" "lambda_dynamodb" {
  role       = aws_iam_role.lambda_resume_counter.name
  policy_arn = aws_iam_policy.lambda_dynamodb_counter.arn
}

# Attach CloudWatch Logs policy to role (AWS managed)
resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_resume_counter.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Lambda Function
resource "aws_lambda_function" "resume_counter" {
  function_name    = var.lambda_function_name
  role             = aws_iam_role.lambda_resume_counter.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.12"

  # ローカルの zip ファイルから関数コードをアップロード
  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256

  timeout     = 3
  memory_size = 128

  # 依存リソース
  depends_on = [
    aws_iam_role_policy_attachment.lambda_basic_execution,
    aws_iam_role_policy_attachment.lambda_dynamodb,
  ]
}

# CloudWatch Logs グループ (Lambda 用)
resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/${aws_lambda_function.resume_counter.function_name}"
  retention_in_days = 7  # コスト最適化のため 7 日間
}