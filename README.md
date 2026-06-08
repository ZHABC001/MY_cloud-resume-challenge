# Cloud Resume Challenge - SRE Edition

![Tests](https://github.com/ZHABC001/MY_cloud-resume-challenge/actions/workflows/test.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Terraform](https://img.shields.io/badge/Terraform-Managed-7B42BC.svg)
![AWS](https://img.shields.io/badge/AWS-S3%20%7C%20Lambda%20%7C%20DynamoDB-FF9900.svg)

27卒 SRE / インフラエンジニア志望者向けのクラウドポートフォリオです。

## 概要

The Cloud Resume Challenge を AWS 上で実装したプロジェクトです。  
履歴書サイトの静的ホスティング、訪問者カウンター、監視、CI、IaC に加えて、Gemini API を利用した **AI Cloud Portfolio Assistant** を追加しました。

SRE / インフラエンジニアの観点から、以下を重視しています。

* サーバーレス構成
* 可観測性
* コスト最適化
* IAM 最小権限
* API キーをフロントエンドに公開しない設計
* 不正利用対策とリクエストログ管理

## Live Demo

* メイン: https://zhabc001.me
* S3 直接アクセス: http://resume.zhangbeichuan.s3-website-ap-northeast-1.amazonaws.com

  * S3 直接アクセスは検証用です。CORS は本番ドメイン中心に制限しているため、一部機能が動作しない場合があります。

\---

## アーキテクチャ

```text
\[User Browser]
    |
    | HTTPS
    v
\[Cloudflare CDN]
    |
    | Flexible SSL / Cache / DDoS Protection
    v
\[S3 Static Website Hosting]
    |
    | HTML / CSS / JavaScript
    v
\[Portfolio Website]
```

### Visitor Counter Flow

```text
\[Browser JavaScript]
    |
    | GET /counter
    v
\[API Gateway]
    |
    v
\[Lambda: cloud-resume-counter]
    |
    | DynamoDB Atomic Counter
    v
\[DynamoDB: cloud-resume-counter]
```

### AI Assistant Flow

```text
\[Browser JavaScript]
    |
    | POST /ask
    v
\[API Gateway]
    |
    v
\[Lambda: ai-assistant-api]
    |
    | Gemini API call
    v
\[Gemini API]

\[Lambda: ai-assistant-api]
    |
    | Request metadata log
    v
\[DynamoDB: ai\_assistant\_logs]
```

### Monitoring / Operations

* CloudWatch Logs: Lambda 実行ログ
* CloudWatch Alarm: Lambda Errors > 0 を監視
* SNS: ALARM 状態のみメール通知
* GitHub Actions: backend 変更時に pytest を自動実行
* Terraform: 主要 AWS リソースを IaC 管理

\---

## 使用技術

|カテゴリ|技術|
|-|-|
|Cloud|AWS S3, Lambda, DynamoDB, API Gateway, CloudWatch, IAM|
|CDN / HTTPS|Cloudflare Free Plan|
|Frontend|HTML, CSS, JavaScript, Bootstrap|
|Backend|Python 3.12|
|AI API|Gemini API|
|IaC|Terraform|
|Testing|pytest, moto|
|CI/CD|GitHub Actions|
|DNS|Namecheap → Cloudflare|

\---

## 実装済み機能

### Frontend

* HTML / CSS による履歴書ページ
* JavaScript による訪問者カウンター表示
* AI Assistant UI
* Gemini API の利用上の注意を表示

### Backend

* Lambda + API Gateway による `/counter` API
* DynamoDB Atomic Counter による訪問者カウンター
* Lambda + API Gateway による `/ask` API
* Gemini API をバックエンド側から呼び出す AI Assistant
* DynamoDB による AI Assistant リクエストメタデータ記録

### Infrastructure / Operations

* S3 静的ウェブサイトホスティング
* Cloudflare による HTTPS 化、CDN、DDoS 防護
* CloudWatch Logs
* CloudWatch Alarm + SNS 通知
* IAM 最小権限ポリシー
* GitHub Actions CI
* Terraform による IaC 管理

\---

## AI Cloud Portfolio Assistant

Cloud Resume Challenge のポートフォリオサイトに、AI Assistant 機能を追加しました。  
訪問者は AWS 構成、使用技術、Cloud Resume Challenge の実装内容、面接向け説明などについて質問できます。

### 主な機能

* ポートフォリオや AWS 構成に関する質問への回答
* 日本語・英語・中国語の質問に対応
* Gemini API をバックエンド側から呼び出し
* API キーをフロントエンドに公開しない設計
* 不正利用防止とコスト管理のためのリクエストログ記録
* 個人情報や機密情報の送信を避けるための利用上の注意を表示

### セキュリティ設計

* Gemini API キーは Lambda の環境変数で管理
* フロントエンドから Gemini API を直接呼び出さない
* CORS を許可された Origin に制限
* 入力文字数を 500 文字以内に制限
* 回答範囲をポートフォリオ関連に限定
* IP アドレスはそのまま保存せず、ソルト付きハッシュとして記録
* 質問本文はログに保存しない

### コスト管理

* 低コストの Gemini モデルを使用
* 出力トークン数を制限
* DynamoDB にリクエストメタデータを記録
* DynamoDB TTL により古いログを自動削除
* 将来的に IP ベースの日次制限や回答キャッシュを追加予定

### DynamoDB ログ

AI Assistant では、必要最小限のリクエストメタデータのみを記録しています。

|項目|内容|
|-|-|
|request\_id|リクエストごとの一意 ID|
|created\_at|Unix timestamp|
|created\_at\_iso|UTC 時刻|
|expires\_at|TTL 用の有効期限|
|ip\_hash|ハッシュ化された IP|
|user\_agent|User-Agent の一部|
|question\_length|質問文字数|
|status|success / error など|

質問本文や生の IP アドレスは保存していません。

\---

## SRE 観点での設計考慮事項

### 可観測性

* CloudWatch Logs による Lambda 実行ログ
* CloudWatch Alarm による Errors > 0 監視
* SNS 経由のメール通知
* ALARM 状態のみ通知することで Alert Fatigue を軽減

### コスト最適化

* AWS Free Tier / Always Free 枠を活用
* Cloudflare Free Plan を利用
* DynamoDB は小規模アクセスに適した構成
* Gemini API は低コストモデルを利用
* 月額予算アラートを設定
* ログは TTL により自動削除

### セキュリティ

* IAM 最小権限の原則
* Lambda は必要な DynamoDB 操作のみ許可
* API キーをフロントエンドに置かない
* CORS によるクロスオリジン制御
* Cloudflare による DDoS 防護
* リクエストログでは IP をハッシュ化

\---

## Cloudflare HTTPS 化の決断

### 状況

当初は AWS CloudFront による HTTPS 化を計画していましたが、AWS アカウントの検証ティケットが長期間未対応となり、締切までに完了できないリスクがありました。

### 代替案の検討

|選択肢|メリット|デメリット|
|-|-|-|
|AWS CloudFront|AWS ネイティブ、統合管理|アカウント検証待ち、締切リスク|
|Cloudflare|即時利用可能、無料、業界標準|AWS リソースとの統合性は CloudFront より弱い|
|HTTP のみ|構成が簡単|HTTPS なしで応募作品として不十分|

### 採用理由

1. 締切までに HTTPS 化を完了できる
2. Cloudflare CDN + AWS Backend は実運用でも一般的な構成
3. 将来的に CloudFront へ切り替え可能
4. Cloudflare Free Plan で低コストに運用できる

### SRE 観点での学び

* 固定観念にとらわれず代替案を検討する重要性
* 可逆性を意識した設計
* ベンダーロックインを避ける設計判断

\---

## 技術的こだわりポイント

### 1\. DynamoDB Atomic Counter

```python
table.update\_item(
    Key={"id": "visitor\_count"},
    UpdateExpression="ADD #count :inc",
    ExpressionAttributeNames={"#count": "count"},
    ExpressionAttributeValues={":inc": 1},
    ReturnValues="UPDATED\_NEW"
)
```

`ADD` operation を使うことで、複数のユーザーが同時にアクセスしても race condition なく count をインクリメントできます。

なお、現在のカウンターはユニークユーザー数ではなく、ページ読み込みごとの page view count として実装しています。

### 2\. Lambda パフォーマンス最適化

```python
dynamodb = boto3.resource("dynamodb", region\_name="ap-northeast-1")
table = dynamodb.Table("cloud-resume-counter")

def lambda\_handler(event, context):
    table.update\_item(...)
```

DynamoDB クライアントを関数外で初期化し、ウォームスタート時の初期化コストを削減しています。

### 3\. CORS 多層防御

* API Gateway 側で CORS を設定
* Lambda レスポンスにも CORS headers を設定
* 本番では Allow-Origin を本番ドメイン中心に制限

### 4\. IAM 最小権限

```json
{
  "Version": "2012-10-17",
  "Statement": \[
    {
      "Effect": "Allow",
      "Action": \["dynamodb:UpdateItem"],
      "Resource": "arn:aws:dynamodb:ap-northeast-1:\*:table/cloud-resume-counter"
    }
  ]
}
```

`AmazonDynamoDBFullAccess` ではなく、必要な操作だけに絞った権限を付与しています。

### 5\. AI Assistant の API キー保護

Gemini API キーは HTML / JavaScript には記述せず、Lambda の環境変数で管理しています。  
フロントエンドは API Gateway の `/ask` にのみリクエストを送り、外部 AI API への直接アクセスは行いません。

\---

## Infrastructure as Code

主要な AWS リソースは Terraform で IaC 化しています。  
ただし、AI Assistant 関連の新規リソースは拡張実装として追加したため、現時点では一部手動作成のリソースを含みます。今後 Terraform 管理へ統合する予定です。

### 既存 Terraform 管理対象

|リソース種別|内容|
|-|-|
|S3|静的ウェブサイト用 bucket / 設定|
|DynamoDB|訪問者カウンター用テーブル|
|Lambda|訪問者カウンター関数|
|IAM|Lambda 実行ロール、最小権限ポリシー|
|CloudWatch Logs|Lambda 用ロググループ|
|API Gateway|counter API route / integration / stage|
|Archive|Lambda コード zip パッケージ|

### 今後 Terraform 化予定

* Gemini API キー用の Secrets Manager 管理
* IP ベースの日次制限用 DynamoDB table

### Terraform の活用ポイント

#### 1\. 既存リソースの取り込み

手動で作成済みの AWS リソースを `terraform import` で段階的に Terraform 管理下へ移行しました。

```bash
terraform import aws\_s3\_bucket.resume resume.zhangbeichuan
terraform import aws\_dynamodb\_table.visitor\_counter cloud-resume-counter
terraform import aws\_lambda\_function.resume\_counter cloud-resume-counter
```

これにより、既存の本番リソースを再作成するリスクを避けながら IaC 化を進めました。

#### 2\. デフォルトタグによる一元管理

```hcl
provider "aws" {
  default\_tags {
    tags = {
      Project     = var.project\_name
      Environment = var.environment
      Owner       = var.owner
      ManagedBy   = "Terraform"
    }
  }
}
```

全リソースに `ManagedBy = Terraform` タグを自動付与し、手動変更の追跡をしやすくしました。

#### 3\. リソース間参照

```hcl
resource "aws\_iam\_policy" "lambda\_dynamodb\_counter" {
  policy = jsonencode({
    Statement = \[{
      Resource = aws\_dynamodb\_table.visitor\_counter.arn
    }]
  })
}
```

ARN をハードコードせず、Terraform のリソース参照で動的に解決しています。

#### 4\. 自動コードパッケージング

```hcl
data "archive\_file" "lambda\_zip" {
  type        = "zip"
  source\_file = "${path.module}/../backend/lambda/lambda\_function.py"
  output\_path = "${path.module}/lambda\_function.zip"
}
```

Lambda コード変更時、Terraform が zip を再作成し、`source\_code\_hash` により変更を検知します。

### 使い方

```bash
cd terraform
terraform init
terraform plan
terraform apply
terraform destroy
```

\---

## Testing \& CI/CD

### テスト戦略

現在は訪問者カウンター Lambda を中心に、pytest + moto による単体テストを実装しています。

|#|テスト内容|目的|
|-|-|-|
|1|初回アクセスで count=1|基本動作|
|2|複数回アクセスで正しくインクリメント|並行アクセス対策|
|3|レスポンスに CORS ヘッダーが含まれる|API 規約|
|4|Content-Type が application/json|API 規約|
|5|count は int 型|データ型確認|

### モック戦略

```python
@pytest.fixture
def dynamodb\_table(aws\_credentials):
    with mock\_aws():
        dynamodb = boto3.resource("dynamodb", region\_name="ap-northeast-1")
        table = dynamodb.create\_table(...)
        yield table
```

moto で DynamoDB をモック化することで、実 AWS に依存しないテストを実現しています。

### GitHub Actions CI

`.github/workflows/test.yml` で push 時に自動テストを実行します。

```yaml
on:
  push:
    branches: \[main]
    paths:
      - "backend/\*\*"

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install pytest boto3 moto
      - run: pytest backend/tests/ -v
```

### 工夫した点

* `paths` filter により backend 配下の変更時のみ CI を実行
* pip cache により依存関係のインストール時間を削減
* shift-left の考え方で開発初期からテストを実施

\---

## 開発記録

詳細な開発ログは [DEVLOG.md](DEVLOG.md) を参照。

### 開発期間

* 基本構築: 2026/05/02 - 2026/05/15
* AI Assistant 拡張: 2026/05/25 - 2026/05/28

### 主な学習成果

* AWS の主要サービスを統合した end-to-end 構築
* HTTP、CORS、JSON、API Gateway の理解
* Python + boto3 によるサーバーレス開発
* IAM ポリシー設計
* Git / GitHub のワークフロー
* Terraform による IaC 実践
* pytest + GitHub Actions による CI/CD
* Cloudflare を活用した HTTPS 化
* Gemini API を用いた LLM アプリケーション開発
* SRE 観点でのインフラ設計と運用

\---

## ディレクトリ構成

```text
MY\_cloud-resume-challenge/
├── README.md
├── DEVLOG.md
├── ZHANG\_BEICHUAN\_Cloud\_Resume.html
├── css/
├── js/
├── assets/
├── backend/
│   ├── lambda/
│   │   ├── lambda\_function.py
│   │   └── requirements.txt
│   ├── ai\_assistant/
│   │   └── lambda\_function.py
│   └── tests/
│       ├── conftest.py
│       └── test\_lambda\_function.py
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   └── outputs.tf
└── .github/
    └── workflows/
        └── test.yml
```

\---

## Future Improvements

* AI Assistant 関連リソースの Terraform 化
* Gemini API キーを AWS Secrets Manager で管理
* IP ベースの日次リクエスト制限
* DynamoDB による回答キャッシュ
* Cloudflare Turnstile による bot 対策
* CloudFront + ACM による AWS ネイティブ HTTPS 化
* AWS WAF によるアプリケーション層セキュリティ
* X-Ray による分散トレーシング
* pytest-cov によるカバレッジ測定
* AI Assistant Lambda の単体テスト追加
* RAG による README / 履歴書ベースの回答精度向上

\---

## 作者

**張 北川 (ZHANG BEICHUAN)**

* 千葉工業大学 大学院 マネジメント工学専攻（2027年3月卒業予定）
* AWS Certified Solutions Architect - Associate
* JLPT N2
* TOEIC Listening \& Reading 840
* GitHub: [@ZHABC001](https://github.com/ZHABC001)
* Email: qingfengtiansuo@gmail.com

\---

## ライセンス

MIT License

