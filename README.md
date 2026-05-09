# Cloud Resume Challenge - SRE Edition

ビズメイツ向けエンジニア職応募作品

## 概要

The Cloud Resume Challenge を AWS 上で実装したプロジェクト。
SRE / インフラエンジニアの観点から、可観測性とコスト最適化を意識した設計。

**Live Demo**:

* HTTP: http://resume.zhangbeichuan.s3-website-ap-northeast-1.amazonaws.com
* HTTPS: https://zhabc001.me （CloudFront 設定後追加予定）

## アーキテクチャ

```
\[ブラウザ]
    |
    | HTTPS
    v
\[CloudFront] <-- ACM SSL 証明書
    |  (HTTPS 終端 + CDN)
    | OAC
    v
\[S3 Bucket: resume.zhangbeichuan]
   (HTML / CSS / JS)


JS が動的に呼び出し:

\[ブラウザ JS]
    |
    | fetch (CORS)
    v
\[API Gateway: GET /counter]
    |
    v
\[Lambda: cloud-resume-counter] <-- IAM Role (最小権限)
    |
    v
\[DynamoDB: cloud-resume-counter]
   (Atomic Counter)

監視: CloudWatch Logs + Alarms
```

## 使用技術

|カテゴリ|技術|
|-|-|
|Cloud|AWS (S3, Lambda, DynamoDB, API Gateway, CloudWatch, IAM)|
|Frontend|HTML, CSS, JavaScript|
|Backend|Python 3.12|
|IaC|Terraform (追加予定)|
|CI/CD|GitHub Actions (追加予定)|
|DNS|Namecheap|

## 機能

### 実装済み

* HTML/CSS による履歴書ページ
* S3 静的ウェブサイトホスティング
* DynamoDB による訪問者カウンター
* Lambda + API Gateway による REST API
* CORS 設定によるフロント・バック連携
* IAM 最小権限ポリシー
* CloudWatch Logs (保持期間 7 日)

### 実装中・予定

* CloudFront による HTTPS 化 (AWS アカウント検証待ち)
* カスタムドメイン (zhabc001.me) の関連付け
* CloudWatch Alarm によるエラー監視
* Terraform による Infrastructure as Code 化
* pytest + moto による Lambda 単体テスト
* GitHub Actions による CI/CD パイプライン

## SRE 観点での設計考慮事項

### 可観測性

* CloudWatch Logs による Lambda 実行ログ
* ログ保持期間 7 日 (コスト最適化)
* CloudWatch Alarm によるエラー率監視 (実装予定)

### コスト最適化

* AWS Always Free Tier の最大活用
* 全リソースに Standard Tag 付与
* 月額予算アラート設定 ($1)
* 結果: 月額 0 円で運用

### セキュリティ

* IAM 最小権限の原則
* DynamoDB atomic counter による並行アクセス対策
* CORS による Cross-Origin 制御

## 技術的こだわりポイント

### DynamoDB Atomic Counter

ADD operation を使い、複数のユーザーが同時にアクセスしても
race condition なく count が正確にインクリメントされる。

### Lambda パフォーマンス最適化

boto3 クライアントを関数外で初期化し、ウォームスタート時の
初期化コストを削減。レスポンス時間を 5-10 倍速く実現。

### IAM 最小権限

AmazonDynamoDBFullAccess から、特定テーブルへの UpdateItem のみ
許可するカスタムポリシーに変更。

## 開発記録

詳細な開発ログは [DEVLOG.md](DEVLOG.md) を参照。

## 今後の改善計画

* \[ ] CloudFront による HTTPS 化
* \[ ] カスタムドメイン関連付け
* \[ ] CloudWatch Alarm 設定
* \[ ] Terraform 化
* \[ ] pytest 単体テスト
* \[ ] GitHub Actions CI/CD
* \[ ] Lambda 構造化ログ
* \[ ] X-Ray 分散トレーシング (中期)
* \[ ] AWS WAF (中期)

## 作者

**張 北川 (ZHANG BEICHUAN)**

* 千葉工業大学 大学院 マネジメント工学専攻 (2027 年 3 月卒予定)
* AWS Certified Solutions Architect - Associate
* GitHub: [@ZHABC001](https://github.com/ZHABC001)

## ライセンス

MIT License

