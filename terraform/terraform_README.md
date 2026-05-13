# Terraform - Cloud Resume Challenge

このディレクトリは Cloud Resume Challenge プロジェクトの
AWS インフラを Terraform で管理するためのファイルを格納しています。

## ディレクトリ構成

```
terraform/
├── README.md          # このファイル
├── main.tf            # AWS リソース定義
├── variables.tf       # 変数定義
└── outputs.tf         # 出力値定義
```

## 管理対象リソース (17 個)

| カテゴリ | 数 | リソース |
|---------|----|----|
| S3 (resume.zhangbeichuan) | 4 | Bucket, Website Config, Public Access Block, Bucket Policy |
| S3 (zhabc001.me) | 4 | Bucket, Website Config, Public Access Block, Bucket Policy |
| DynamoDB | 1 | visitor_counter テーブル |
| Lambda | 1 | cloud-resume-counter 関数 |
| IAM | 4 | Role, Policy, Role Policy Attachment x 2 |
| CloudWatch Logs | 1 | Lambda 用ロググループ |
| API Gateway | 5 | API, Integration, Route, Stage, Lambda Permission |
| Archive (data) | 1 | Lambda コード zip パッケージ |

## 前提条件

- Terraform >= 1.0
- AWS CLI 認証情報設定済み (`aws configure`)
- AWS リージョン: `ap-northeast-1` (東京)

## 使い方

### 初期化

```bash
terraform init
```

Provider (AWS, Archive) をダウンロードします。

### 変更プレビュー

```bash
terraform plan
```

実際のリソースを変更せず、変更内容を確認します。

### 適用

```bash
terraform apply
```

`yes` で確認後、AWS リソースが作成・更新されます。

### 出力値の確認

```bash
terraform output
```

S3 URL、API Gateway endpoint、Lambda ARN 等を確認できます。

### 全リソース削除 (注意!)

```bash
terraform destroy
```

⚠️ **すべての AWS リソースが削除されます**。データ復旧不可。

## 既存リソースの取り込み (terraform import)

手動で作成済みのリソースを Terraform 管理下に移行する例:

```bash
# S3 桶
terraform import aws_s3_bucket.resume resume.zhangbeichuan

# DynamoDB テーブル
terraform import aws_dynamodb_table.visitor_counter cloud-resume-counter

# Lambda 関数
terraform import aws_lambda_function.resume_counter cloud-resume-counter

# IAM Role
terraform import aws_iam_role.lambda_resume_counter lambda-resume-counter-role

# API Gateway (例)
terraform import aws_apigatewayv2_api.counter_api oq25hly377
```

## 設計のポイント

### 1. デフォルトタグの活用

`provider "aws" { default_tags { ... } }` で全リソースに
自動的にタグを付与しています。

```hcl
default_tags {
  tags = {
    Project     = "cloud-resume-challenge"
    Environment = "production"
    Owner       = "zhang"
    ManagedBy   = "Terraform"
  }
}
```

`ManagedBy = "Terraform"` タグにより、
コンソールから手動変更すべきでないことが明示されます。

### 2. リソース間参照

ARN 等を直接ハードコードせず、リソース参照で動的解決:

```hcl
resource "aws_iam_policy" "lambda_dynamodb_counter" {
  policy = jsonencode({
    Statement = [{
      Resource = aws_dynamodb_table.visitor_counter.arn
    }]
  })
}
```

DynamoDB テーブルの ARN が変わっても、自動的に追従します。

### 3. 自動 Lambda パッケージング

`data "archive_file"` で Lambda コードを自動 zip 化:

```hcl
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/../backend/lambda/lambda_function.py"
  output_path = "${path.module}/lambda_function.zip"
}
```

`source_code_hash` でコード変更を検知し、変更時のみ Lambda が再デプロイされます。

### 4. 最小権限の原則 (IAM)

Lambda の IAM Policy は必要最小限:

```json
{
  "Effect": "Allow",
  "Action": ["dynamodb:UpdateItem"],
  "Resource": "arn:aws:dynamodb:ap-northeast-1:*:table/cloud-resume-counter"
}
```

AmazonDynamoDBFullAccess から、特定テーブルへの UpdateItem のみに制限。

## 既知の課題

### 1. terraform.tfstate のローカル管理

現在 state ファイルはローカルに保存しています。
本番運用では以下が推奨されます:

```hcl
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "cloud-resume-challenge/terraform.tfstate"
    region         = "ap-northeast-1"
    dynamodb_table = "terraform-state-lock"
  }
}
```

S3 backend + DynamoDB lock により、チーム開発で安全に協業できます。

### 2. 環境分離 (dev/staging/prod)

現在 production 環境のみですが、`terraform workspace` を使えば
複数環境を同じコードベースで管理できます。

```bash
terraform workspace new staging
terraform workspace select staging
terraform apply
```

### 3. CI/CD 統合

GitHub Actions で以下を自動化すると更に SRE 的:

- PR 作成時: `terraform plan` を自動実行してコメント
- main マージ時: `terraform apply` を自動実行

## トラブルシューティング

### "Provider not installed" エラー

```bash
terraform init -upgrade
```

新しい Provider が必要な場合、`-upgrade` フラグで強制更新。

### import 時に "Resource already exists"

```bash
# 既に Terraform 管理下にある場合
terraform state list  # 確認
terraform state rm <resource>  # 一旦削除して再 import
```

### plan で意図しない "destroy"

⚠️ **絶対に apply せず**、以下を確認:

1. main.tf の記述と実態に乖離があるか
2. import が正しくできているか
3. リソース参照 (`aws_xxx.yyy.attr`) が正しいか

## 参考リンク

- [Terraform AWS Provider Docs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [terraform import](https://developer.hashicorp.com/terraform/cli/import)
- [Cloud Resume Challenge](https://cloudresumechallenge.dev/)
