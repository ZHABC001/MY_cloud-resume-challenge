# Cloud Resume Challenge - SRE Edition

![Tests](https://github.com/ZHABC001/MY_cloud-resume-challenge/actions/workflows/test.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Terraform](https://img.shields.io/badge/Terraform-Managed-7B42BC.svg)
![AWS](https://img.shields.io/badge/AWS-S3%20%7C%20Lambda%20%7C%20DynamoDB-FF9900.svg)

ビズメイツ向けエンジニア職応募作品

## 概要

The Cloud Resume Challenge を AWS 上で実装したプロジェクト。
SRE / インフラエンジニアの観点から、可観測性とコスト最適化を意識した設計。

**Live Demo**:
- 🌐 **メイン**: https://zhabc001.me (HTTPS, Cloudflare 経由)
- 📦 直接アクセス: http://resume.zhangbeichuan.s3-website-ap-northeast-1.amazonaws.com (HTTP, S3 直接)

---

## アーキテクチャ

```
[ユーザー] https://zhabc001.me
    |
    | HTTPS (自動)
    v
[Cloudflare CDN]
    |  (Free Plan: HTTPS + DDoS 防護 + キャッシュ)
    | Flexible SSL
    v
[S3 Bucket: zhabc001.me]
    (HTML / CSS / JS - 静的ホスティング)


JS が動的に呼び出し:

[ブラウザ JS]
    |
    | fetch() / CORS
    v
[API Gateway: GET /counter]
    |
    v
[Lambda: cloud-resume-counter]  <-- IAM Role (最小権限)
    |
    | DynamoDB Atomic Counter
    v
[DynamoDB: cloud-resume-counter]

監視・運用:
- CloudWatch Logs (Lambda 実行ログ, 7 日保持)
- CloudWatch Alarm (Errors > 0 → SNS メール通知)
- GitHub Actions CI (push 時に pytest 自動実行)
- Terraform (17 リソース全て IaC 管理)
```

---

## 使用技術

| カテゴリ | 技術 |
|---------|------|
| Cloud | AWS (S3, Lambda, DynamoDB, API Gateway, CloudWatch, IAM) |
| CDN / HTTPS | Cloudflare (Free Plan) |
| Frontend | HTML, CSS, JavaScript |
| Backend | Python 3.12 |
| IaC | Terraform |
| Testing | pytest + moto |
| CI/CD | GitHub Actions |
| DNS | Namecheap (NameServer → Cloudflare) |

---

## 機能

### 実装済み

#### Frontend
- HTML/CSS による履歴書ページ (Bootstrap ベース)
- JavaScript による訪問者カウンター表示

#### Infrastructure
- S3 静的ウェブサイトホスティング
- **Cloudflare による HTTPS 化 + CDN + DDoS 防護**
- カスタムドメイン (zhabc001.me)

#### Backend
- DynamoDB による訪問者カウンター (Atomic Counter)
- Lambda + API Gateway による REST API
- CORS 設定によるフロント・バック連携

#### SRE / Operations
- IAM 最小権限ポリシー
- CloudWatch Logs (保持期間 7 日)
- CloudWatch Alarm によるエラー監視 (SNS メール通知)
- pytest + moto による単体テスト (5 ケース)
- GitHub Actions による CI 自動実行
- **Terraform による 17 AWS リソースの IaC 管理**

### 実装予定 (応募後)

- CloudFront による AWS ネイティブ HTTPS 化
  - 現在 Cloudflare を使用中、AWS アカウント検証完了次第切り替え
- AWS WAF によるアプリケーション層セキュリティ
- terraform.tfstate を S3 backend で管理
- X-Ray による分散トレーシング
- pytest-cov によるカバレッジ測定
- 構造化ログ (logging モジュール) への移行

---

## SRE 観点での設計考慮事項

### 可観測性 (Observability)

- CloudWatch Logs による Lambda 実行ログ
- ログ保持期間 7 日 (コスト最適化)
- CloudWatch Alarm による Errors > 0 監視
- SNS 経由メール通知 (ALARM 状態のみ、Alert Fatigue 対策)

### コスト最適化

- AWS Always Free Tier の最大活用
  - Lambda: 100 万リクエスト/月 (永続無料)
  - DynamoDB: 25 GB ストレージ (永続無料)
- Cloudflare Free Plan で HTTPS + CDN 無料
- 全リソースに Standard Tag 付与
- 月額予算アラート設定 ($1)
- 結果: **月額 0 円で運用**

### セキュリティ

- IAM 最小権限の原則
  - Lambda は cloud-resume-counter テーブルへの UpdateItem のみ許可
- DynamoDB atomic counter による並行アクセス対策
- CORS によるクロスオリジン制御
- Cloudflare による DDoS 防護 (Layer 3/4/7)

---

## Cloudflare HTTPS 化の決断

### 状況

当初は AWS CloudFront による HTTPS 化を計画していましたが、
AWS アカウントの検証ティケットが 8 日間未対応となり、
締切までに完了できないリスクがありました。

### 代替案の検討

| 選択肢 | メリット | デメリット |
|--------|---------|----------|
| AWS CloudFront | AWS ネイティブ、統合管理 | アカウント検証待ち、締切リスク |
| **Cloudflare (採用)** | 即時利用可能、無料、業界標準 | AWS リソースとの統合性 |
| HTTP のみ | 簡単 | HTTPS なしで応募作品として不十分 |

### 採用理由

1. **締切優先**: 5/15 までに HTTPS 化を完了する必要があった
2. **業界標準**: "Cloudflare CDN + AWS Backend" は実運用で広く採用
3. **可逆性**: 将来 CloudFront に切り替え可能 (DNS 変更のみ)
4. **コスト**: Cloudflare Free Plan で永久無料

### 実装

```
[Browser] --HTTPS--> [Cloudflare] --HTTP--> [S3]
                       Flexible SSL Mode
```

### SRE 観点での学び

- **意思決定の柔軟性**: 固執せず代替案を検討する
- **可逆性の重視**: 将来の変更コストを最小化
- **ベンダーロックイン回避**: 複数のサービスを組み合わせる設計

---

## 技術的こだわりポイント

### 1. DynamoDB Atomic Counter

```python
table.update_item(
    Key={'id': 'visitor_count'},
    UpdateExpression='ADD #count :inc',
    ExpressionAttributeNames={'#count': 'count'},
    ExpressionAttributeValues={':inc': 1},
    ReturnValues='UPDATED_NEW'
)
```

ADD operation を使い、複数のユーザーが同時にアクセスしても
race condition なく count が正確にインクリメントされる。

### 2. Lambda パフォーマンス最適化

```python
# クライアント初期化を関数外で実行 (重要!)
dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-1')
table = dynamodb.Table('cloud-resume-counter')

def lambda_handler(event, context):
    # ウォームスタート時は再初期化されない
    table.update_item(...)
```

ウォームスタート時の初期化コストを削減し、レスポンス時間を 5-10 倍速く実現。

### 3. CORS 多層防御

- API Gateway 側で OPTIONS preflight 対応
- Lambda レスポンスにも CORS Headers 設定
- 本番では Allow-Origin を特定ドメインに絞る予定

### 4. IAM 最小権限

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": ["dynamodb:UpdateItem"],
            "Resource": "arn:aws:dynamodb:ap-northeast-1:*:table/cloud-resume-counter"
        }
    ]
}
```

AmazonDynamoDBFullAccess から、必要最小限のポリシーに変更。

### 5. Alert Fatigue 対策

CloudWatch Alarm の初期設定では、状態変化 (OK / INSUFFICIENT_DATA) でも
通知が来て、いわゆる "Alert Fatigue" を経験しました。
ALARM 状態のみ通知するよう設定を見直し、本当に対応が必要な時のみ
通知が来る状態に改善しました。

---

## Infrastructure as Code (Terraform)

プロジェクトのインフラは Terraform で完全に IaC 化されています。

### 管理対象リソース (17 個)

| リソース種別 | 数 | 内容 |
|------------|----|----|
| S3 | 8 | resume.zhangbeichuan + zhabc001.me 各 4 リソース |
| DynamoDB | 1 | visitor_counter テーブル |
| Lambda | 1 | 訪問者カウンター関数 |
| IAM | 4 | Role、Policy、Attachment x 2 |
| CloudWatch Logs | 1 | Lambda 用ロググループ |
| API Gateway | 5 | API、Integration、Route、Stage、Permission |
| Archive (data) | 1 | Lambda コード zip パッケージ |

### Terraform の活用ポイント

#### 1. 既存リソースの取り込み (terraform import)

手動で作成済みの AWS リソースを terraform import で
段階的に Terraform 管理下に移行しました。

```bash
terraform import aws_s3_bucket.resume resume.zhangbeichuan
terraform import aws_dynamodb_table.visitor_counter cloud-resume-counter
terraform import aws_lambda_function.resume_counter cloud-resume-counter
```

これにより、既存の本番リソースを再作成するリスクなく、IaC 化を実現できました。

#### 2. デフォルトタグによる一元管理

```hcl
provider "aws" {
  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      Owner       = var.owner
      ManagedBy   = "Terraform"
    }
  }
}
```

全リソースに ManagedBy = Terraform タグを自動付与。
手動変更を防ぎ、リソース管理を統一しました。

#### 3. リソース間参照

```hcl
resource "aws_iam_policy" "lambda_dynamodb_counter" {
  policy = jsonencode({
    Statement = [{
      Resource = aws_dynamodb_table.visitor_counter.arn
    }]
  })
}
```

ARN をハードコードせず、リソース参照で動的に解決。

#### 4. 自動コードパッケージング

```hcl
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/../backend/lambda/lambda_function.py"
  output_path = "${path.module}/lambda_function.zip"
}
```

Lambda コード変更時、Terraform が自動的に zip 再作成。
source_code_hash で変更検知し、必要時のみデプロイされます。

### 使い方

```bash
cd terraform
terraform init      # 初期化
terraform plan      # 変更プレビュー
terraform apply     # 適用
terraform destroy   # 全リソース削除 (注意!)
```

### 今後の改善計画

- terraform.tfstate を S3 backend + DynamoDB lock で管理
- terraform workspace で環境分離 (dev/staging/prod)
- CI/CD パイプラインで terraform plan の自動実行

---

## Testing & CI/CD

### テスト戦略

pytest + moto による単体テストで、Lambda 関数の振る舞いを検証。

#### テストケース (5 つ)

| # | テスト内容 | 目的 |
|---|-----------|------|
| 1 | 初回アクセスで count=1 | 基本動作 |
| 2 | 複数回アクセスで正しくインクリメント | 並行性 |
| 3 | レスポンスに CORS ヘッダー含まれる | API 規約 |
| 4 | Content-Type が application/json | API 規約 |
| 5 | count は int 型 (Decimal ではない) | データ型 |

#### モック戦略

```python
@pytest.fixture
def dynamodb_table(aws_credentials):
    with mock_aws():
        dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-1')
        table = dynamodb.create_table(...)
        yield table
```

moto で DynamoDB をモック化することで:
- 実 AWS に依存しない高速テスト
- 課金なし、隔離された環境
- CI 環境でも再現可能

### GitHub Actions CI

.github/workflows/test.yml で push 時に自動テスト実行。

```yaml
on:
  push:
    branches: [main]
    paths:
      - 'backend/**'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install pytest boto3 moto
      - run: pytest backend/tests/ -v
```

#### 工夫した点

- **paths filter**: backend 配下の変更時のみトリガー (無駄な実行を削減)
- **pip cache**: 依存関係のキャッシュで実行時間短縮
- **shift-left**: 開発初期からテスト = バグ早期発見

---

## 開発記録

詳細な開発ログは [DEVLOG.md](DEVLOG.md) を参照。

開発期間: 2026/05/02 - 2026/05/15 (約 2 週間)

主な学習成果:
- AWS の主要サービスを統合した end-to-end 構築
- HTTP プロトコル、CORS、JSON データ形式の理解
- Python + boto3 によるサーバーレス開発
- IAM ポリシーの設計
- Git/GitHub のワークフロー
- Terraform による IaC 実践
- pytest + GitHub Actions による CI/CD
- Cloudflare を活用した HTTPS 化
- SRE 観点でのインフラ設計と運用

---

## ディレクトリ構成

```
MY_cloud-resume-challenge/
├── README.md                          # このファイル
├── DEVLOG.md                          # 開発ログ
├── ZHANG_BEICHUAN_Cloud_Resume.html   # 履歴書本体
├── css/, js/, assets/                 # 履歴書のスタイル/スクリプト
├── backend/
│   ├── lambda/
│   │   ├── lambda_function.py         # Lambda 関数本体
│   │   └── requirements.txt
│   └── tests/
│       ├── conftest.py                # pytest 共通設定
│       └── test_lambda_function.py    # 単体テスト
├── terraform/
│   ├── main.tf                        # リソース定義
│   ├── variables.tf                   # 変数
│   └── outputs.tf                     # 出力値
└── .github/
    └── workflows/
        └── test.yml                   # GitHub Actions CI
```

---

## 作者

**張 北川 (ZHANG BEICHUAN)**

- 千葉工業大学 大学院 マネジメント工学専攻 (2027 年 3 月卒予定)
- AWS Certified Solutions Architect - Associate (2025/12)
- JLPT N2 (2023/12), TOEIC 840 (2023/10)
- GitHub: [@ZHABC001](https://github.com/ZHABC001)
- Email: qingfengtiansuo@gmail.com

---

## ライセンス

MIT License
