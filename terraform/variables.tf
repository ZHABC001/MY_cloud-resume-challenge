# 文件: terraform/variables.tf

variable "aws_region" {
  description = "AWS リージョン"
  type        = string
  default     = "ap-northeast-1"
}

variable "project_name" {
  description = "プロジェクト名"
  type        = string
  default     = "cloud-resume-challenge"
}

variable "environment" {
  description = "環境名 (dev/staging/production)"
  type        = string
  default     = "production"
}

variable "owner" {
  description = "リソースの所有者"
  type        = string
  default     = "zhang"
}

variable "s3_bucket_name" {
  description = "履歴書サイト用の S3 バケット名"
  type        = string
  default     = "resume.zhangbeichuan"
}

variable "dynamodb_table_name" {
  description = "訪問者カウンター用の DynamoDB テーブル名"
  type        = string
  default     = "cloud-resume-counter"
}

variable "lambda_function_name" {
  description = "訪問者カウンター用の Lambda 関数名"
  type        = string
  default     = "cloud-resume-counter"
}

variable "gemini_api_key" {
  description = "Gemini API key for AI Assistant"
  type        = string
  sensitive   = true
}

variable "ip_hash_salt" {
  description = "Salt for hashing IP addresses"
  type        = string
  sensitive   = true
}

variable "allowed_origins" {
  description = "Allowed CORS origins for AI Assistant"
  type        = list(string)
  default = [
    "https://zhabc001.me",
    "http://localhost:5500",
    "http://127.0.0.1:5500"
  ]
}