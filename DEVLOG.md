# 開発ログ (Development Log)

Cloud Resume Challenge プロジェクトの日次開発記録。

開発期間: 2026/05/02 - 2026/05/28

- 初期版: 2026/05/02 - 2026/05/15
- AI Assistant 拡張: 2026/05/25 - 2026/05/28

---

## 2026/05/02 (土) - Day 1: プロジェクト立ち上げ

### やったこと

* GitHub アカウント作成および Student Developer Pack 申請
* リポジトリ `MY_cloud-resume-challenge` を作成 (Public、MIT License)
* Git for Windows をインストール、ユーザー設定完了
* SSH キー (ed25519) を生成し、GitHub に登録

  * 認証テスト `ssh -T git@github.com` 成功
* ローカルにリポジトリを clone
* HTML テンプレート `startbootstrap-resume-gh-pages` を選定し配置
* 初回 commit + push を完了

### 学んだこと

* Git の基本ワークフロー (add → commit → push)
* SSH 公開鍵認証の仕組み
* Conventional Commits 形式 (feat / fix / docs / etc.)
* GitHub の Public / Private リポジトリの違い
* Git Bash 環境での Windows パスの適切なエスケープ処理

### 明日やること

* HTML テンプレートの内容を自分の経歴に書き換え
* セクションごとの調整 (About, Projects, Education, Skills, Interests, Certifications)

---

## 2026/05/03 (日) - Day 2: 履歴書コンテンツ作成

### やったこと

* `index.html` を `ZHANG_BEICHUAN_Cloud_Resume.html` にリネーム
* 全セクションのコンテンツを日本語で書き換え:

  * About: 自己紹介文 (建築工学から IT 転身、AWS SAA、観察力・計画力)
  * Projects: Cloud Resume Challenge + マルチクラウド MTD 研究
  * Education: 大学院、語学学校、本科、高校の 4 段階
  * Skills: 技術スタック / 技術詳細 / 言語能力 (日本語統一)
  * Interests: 料理趣味
  * Certifications: AWS SAA, JLPT N2, TOEIC 840 (取得年月付き)
* Navigation の項目を日本語化
* Navbar の背景色を AWS ブランドカラー `#232F3E` にカスタマイズ
* Social icons を整理し、GitHub のみ表示

  * `target="_blank"` および `rel="noopener noreferrer"` でセキュリティ対策
* 個人情報 (住所、電話番号) を削除
* 誤字修正 (クラウト → クラウド)

### つまずいた点

* Languages リストで `fa-ul` を使ったが、図標を入れ忘れて表示が崩れた
* Skills の小見出しの統一性 (英語/日本語混在)

  * 全て日本語に統一して解決

### 学んだこと

* HTML の基本構造 (`<head>`, `<body>`, `<section>`)
* セマンティック要素の意義
* Bootstrap のユーティリティクラス (`mb-5`, `d-flex`, `flex-md-row`, `text-primary`)
* Font Awesome 図標の使い方
* `target="_blank"` 使用時に `rel="noopener noreferrer"` を併記する理由
* Public リポジトリには個人情報を載せない重要性

---

## 2026/05/04 (月) - Day 3: AWS S3 静的サイトホスティング

### やったこと

* AWS Billing Alert を設定 (月額 $1 で通知)
* S3 バケットを作成

  * バケット名: `resume.zhangbeichuan`
  * リージョン: `ap-northeast-1` (東京)
  * パブリックアクセスブロックを解除
* 履歴書ファイル一式をアップロード
* 静的ウェブサイトホスティングを有効化
* バケットポリシーで公開読み取り権限を付与
* Standard Tag を付与:

  * `Project: cloud-resume-challenge`
  * `Environment: production`
  * `Owner: zhang`
* ブラウザから S3 ウェブサイトエンドポイント経由でアクセスを確認

### 学んだこと

* S3 のオブジェクトストレージとしての仕組み
* 静的ウェブサイトホスティング機能の使い方
* パブリックアクセスブロックとバケットポリシーの関係性
* バケットポリシーの JSON 構文 (Effect, Principal, Action, Resource)
* リージョン選定の重要性
* AWS リソースに Standard Tag を付ける SRE のベストプラクティス
* S3 ウェブサイトエンドポイントは HTTP のみ対応

### 課題・改善点

* S3 直接エンドポイントは HTTP のため、CloudFront で HTTPS 化が必要

---

## 2026/05/05 (火) - CloudFront 試行 & ブロック

### やったこと

* CloudFront ディストリビューション作成を試行
* 以下のエラーで作成不可:

  * "Your account must be verified before you can add new CloudFront resources"
* AWS Support にアカウント検証リクエストを提出 (英語で記述)

### 学んだこと

* 新規 AWS アカウントは CloudFront 等の一部サービスで追加検証が必要
* AWS Support の活用方法 (無料の Basic Support でも対応可)
* 締切に向けたリスク管理: 代替案を早めに検討する重要性

### 明日やること

* AWS Support 対応待ち、その間にバックエンド (Lambda + DynamoDB) を進める

---

## 2026/05/07 (木) - Day 4: Lambda + DynamoDB バックエンド

### やったこと

* DynamoDB テーブル `cloud-resume-counter` を作成

  * パーティションキー: `id` (String)
  * 初期データ: `{id: "visitor_count", count: 0}`
* IAM Role `lambda-resume-counter-role` を作成

  * AWSLambdaBasicExecutionRole + AmazonDynamoDBFullAccess
  * (応急版、後で最小権限に変更予定)
* Lambda Function `cloud-resume-counter` を作成

  * Runtime: Python 3.12
  * 訪問者カウンター実装 (atomic counter)
* Lambda コンソールでテスト実行、count がインクリメントされることを確認
* CloudWatch Logs で実行ログを確認

### 学んだこと

* Lambda の基本構造 (`def lambda_handler(event, context)`)
* boto3 でのリソースクライアント初期化
* DynamoDB atomic counter の重要性

  * `ADD` operation で race condition を回避
* Lambda 関数外でクライアント初期化する理由

  * ウォームスタート時の初期化コスト削減 (5-10 倍速い)
* IAM Role と Lambda の関係 (信頼ポリシー)
* CloudWatch Logs による Lambda のログ管理

### つまずいた点

* Decimal 型 → JSON シリアライズエラー

  * 解決: `int(response['Attributes']['count'])` で変換

### 明日やること

* API Gateway を作成して Lambda を HTTP エンドポイント化
* フロントエンドから API を呼び出して訪問者数を表示

---

## 2026/05/08 (金) - Day 5: API Gateway + フロントエンド連携

### やったこと

* API Gateway HTTP API 作成

  * 名前: `cloud-resume-api`
  * ルート: `GET /counter`
  * Lambda 関数 `cloud-resume-counter` と統合
* CORS 設定

  * Allow-Origin: `*` (応急版、本番では絞る予定)
  * Allow-Methods: `GET, OPTIONS`
  * Allow-Headers: `content-type`
* フロントエンド側に訪問者カウンター実装

  * HTML の About セクションに表示位置追加
  * JavaScript の fetch() で API 呼び出し
  * エラーハンドリング (catch + N/A 表示)
* S3 にアップロードし、動作確認
* End-to-end の通信フローを検証成功

### つまずいた点

* ローカル `file://` で HTML を開いた時に CORS エラー

  * origin が `'null'` になり、API Gateway が拒否
  * 解決: S3 にアップロードして `http://` URL でアクセス
* API URL に `/counter` を付け忘れて 404

  * 解決: 完全な URL を確認

### 学んだこと

* API Gateway HTTP API vs REST API の違い

  * HTTP API: シンプル、安い ($1/100万リクエスト)
  * REST API: 高機能、$3.50/100万リクエスト
* Same-Origin Policy と CORS のしくみ
* OPTIONS preflight リクエストの重要性
* `file://` と `http://` で origin の扱いが違う
* fetch() API の使い方 (Promise チェーン)

### 完成したシステム

End-to-end で動作する Web アプリケーション:

```
[ブラウザ] → [S3 静的サイト] → JS が fetch → [API Gateway] → [Lambda] → [DynamoDB]
```

---

## 2026/05/09 (土) - Day 6: SRE 加分項 (IAM 最小権限 + CloudWatch)

### やったこと

* IAM 最小権限の実装

  * カスタム IAM Policy `LambdaResumeCounterDynamoDBPolicy` 作成
  * `dynamodb:UpdateItem` のみ、特定テーブルに対してのみ許可
  * `AmazonDynamoDBFullAccess` を Lambda Role から削除
* CloudWatch Logs の保持期間設定

  * `/aws/lambda/cloud-resume-counter` を 7 日に変更 (コスト最適化)
* CloudWatch Alarm 作成

  * メトリクス: Lambda Errors
  * 閾値: Errors > 0 (5 分間)
  * SNS Topic `cloud-resume-alerts` を作成、メール購読

### 学んだこと

* 最小権限の原則 (Principle of Least Privilege)
* IAM Policy の JSON 構文 (Effect, Action, Resource)
* CloudWatch Logs の保持期間設定によるコスト最適化
* CloudWatch Alarm + SNS の連携
* SNS Subscription Confirmation の仕組み

### つまずいた点

* CloudWatch メトリクス検索で `cloud-resume-counter` がヒットしない

  * 原因: ハイフン区切りで token 化されるため
  * 解決: `Lambda` で検索すれば名前空間が見つかる

### 明日やること

* pytest + moto による Lambda 単体テスト
* GitHub Actions による CI 自動化

---

## 2026/05/10 (日) - Day 7: pytest + GitHub Actions

### やったこと

#### Lambda コードの整理

* `backend/` ディレクトリ構成を作成

  * `backend/lambda/lambda_function.py` (Lambda コード)
  * `backend/tests/test_lambda_function.py` (テストコード)
  * `backend/tests/conftest.py` (pytest 共通設定)

#### pytest 単体テスト実装

* moto による AWS DynamoDB のモック化
* 5 つのテストケース実装:

  1. 初回アクセスで count=1
  2. 複数回アクセスのインクリメント
  3. CORS ヘッダーの存在
  4. Content-Type が JSON
  5. count が int 型 (Decimal ではない)
* ローカルで全テスト合格確認

#### GitHub Actions CI/CD

* `.github/workflows/test.yml` 作成
* main ブランチへの push で自動テスト実行
* `backend/` 配下の変更時のみトリガー (paths filter)
* pip キャッシュで実行時間短縮
* Push 後、GitHub Actions で全テスト合格確認

#### その他

* `.gitignore` 作成 (venv, `__pycache__` 等を除外)
* PyCharm Professional に切り替え (JetBrains 学生ライセンス)

### 学んだこと

* pytest の基本構造 (test_ プレフィックス、fixture)
* moto による AWS サービスのモック化
* フィクスチャー (@pytest.fixture) で共通セットアップ
* GitHub Actions の YAML 構文
* ワークフロートリガー (push, pull_request, paths)
* 依存関係のキャッシング戦略

### SRE 観点での価値

#### Shift Left (テストを早く書く)

* 開発初期からテスト = バグの早期発見

#### 自動化

* 手動テスト → 完全自動化
* 高速フィードバックループ

#### 信頼性

* 5 つのテストケースで主要パスをカバー
* リグレッション (退化) を防止

### 課題・改善点

* pytest-cov でテストカバレッジ計測
* 異常系テスト追加 (DynamoDB エラー時)
* 統合テスト (API Gateway 経由)

---

## 2026/05/11 (月) - Day 8: Terraform IaC 化

### やったこと

#### Phase 1: 環境準備

* Terraform v1.x をインストール
* AWS CLI 認証情報を設定
* `terraform/` ディレクトリ構成を作成

  * `main.tf` (リソース定義)
  * `variables.tf` (変数定義)
  * `outputs.tf` (出力定義)

#### Phase 2: S3 リソースを IaC 化

* S3 バケット、静的ホスティング、公開設定、バケットポリシー
* `terraform import` で既存リソースを取り込み
* `terraform apply` で ManagedBy タグを追加

#### Phase 3: DynamoDB を IaC 化

* `visitor_counter` テーブル定義
* `billing_mode: PAY_PER_REQUEST`

#### Phase 4: Lambda + IAM を IaC 化

* IAM Role (lambda 信頼ポリシー)
* IAM Policy (最小権限: `dynamodb:UpdateItem` のみ)
* Lambda Function (`data archive_file` で自動 zip 化)
* CloudWatch Logs Group (retention 7 日)

#### 合計 12 個の AWS リソースを IaC 化

### 学んだこと

* Terraform 基本概念 (Provider, Resource, Data, Variables, Outputs)
* `terraform init / plan / apply / destroy / import`
* `default_tags` + `ManagedBy = Terraform` でリソース管理
* リソース間参照 (`aws_dynamodb_table.visitor_counter.arn`)
* `terraform import` で既存リソースの取り込み

### つまずいた点

* `archive` provider 追加時の `init -upgrade` 必要
* PowerShell では `\\` 続行が機能せず、Git Bash 推奨
* IAM Role の手動作成時のタグ誤字 ("Project " 末尾空白)
* Lambda Runtime のドリフト (3.14 vs 3.12)

### SRE 観点での価値

* Infrastructure as Code による再現性確保
* バージョン管理 (Git) でインフラ変更履歴
* 手動操作のミス削減
* レビュー可能性 (PR)

### 課題・改善点

* API Gateway の IaC 化 (明日)
* `terraform.tfstate` の S3 backend 化 (チーム開発標準)
* terraform workspace で環境分離

---

## 2026/05/12 (火) - Day 9: API Gateway IaC + Cloudflare HTTPS

### やったこと

#### Phase 1: API Gateway を IaC 化

* HTTP API 本体 (`cloud-resume-api`)
* Lambda Integration (AWS_PROXY)
* Route (`GET /counter`)
* Stage (`$default`, auto_deploy)
* Lambda Permission
* 既存リソースを `terraform import` で取り込み

#### Phase 2: Cloudflare による HTTPS 化

* Cloudflare Free プラン登録
* `zhabc001.me` を Cloudflare に追加
* Namecheap の NameServer を Cloudflare に変更
* DNS 設定:

  * CNAME `@` → S3 (Proxied)
  * CNAME `www` → S3 (Proxied)
* SSL/TLS モード: Flexible
* Always Use HTTPS 有効化

#### Phase 3: S3 桶名問題の解決

* 当初の 404 NoSuchBucket エラー対応
* 原因: S3 が Host header で桶名を判定

  * `zhabc001.me` という名前の桶を探す → 存在しない
* 解決: `zhabc001.me` という名前の S3 桶を新規作成
* Terraform で IaC 化
* AWS CLI で旧桶からファイルを同期
* Cloudflare DNS を新桶に向ける

### 最終的なアーキテクチャ

```
[ユーザー] https://zhabc001.me
   → [Cloudflare CDN + HTTPS]
   → [S3: zhabc001.me]

JS が動的に呼び出し:
[ブラウザ JS]
   → [API Gateway]
   → [Lambda]
   → [DynamoDB]
```

### 学んだこと

#### Cloudflare

* Cloudflare Free プランで HTTPS 化が可能
* SSL/TLS Flexible モードの仕組み
* "Proxied" (橙色雲) vs "DNS Only" (灰色雲) の違い
* CNAME flattening (root domain で CNAME 可能)

#### S3 静的ホスティングの特性

* S3 は Host header で桶を判定
* カスタムドメインを使う場合、桶名 = ドメイン名 が必要

#### SRE 観点

* "CloudFront にこだわらず代替案を検討する柔軟性"
* "ベンダーロックイン回避" の視点
* 旧桶を残す段階的移行戦略

---

## 2026/05/13 (水) - Day 10: Alert Fatigue 対策 + README 整理

### やったこと

#### CloudWatch Alarm の通知設定調整

* OK / INSUFFICIENT_DATA 通知をオフ
* ALARM 状態のみメール通知に変更
* "Alert Fatigue" 対策の実践

#### README.md の大幅リファクタリング

* 過去の編集で壊れた Markdown 構造を整理
* 「Cloudflare HTTPS 化の決断」章節を追加
* 「Testing & CI/CD」章節を追加
* 「ディレクトリ構成」章節を追加
* 4 つのバッジ追加 (Tests, License, Terraform, AWS)

#### terraform/README.md の作成

* 17 リソースの一覧
* `terraform import` の手順
* 設計のポイント (default_tags, リソース間参照等)
* トラブルシューティング

### 学んだこと

* Alert Fatigue は SRE で実在する課題
* 通知の Signal/Noise 比を意識する重要性
* ALARM 状態のみ通知 = "対応が必要な通知のみ" という原則
* README はプロジェクトの「顔」、整理が重要

### つまずいた点

* README に過去の編集で `#` の連発、重複章節、エスケープエラー等が散在
* 部分修正より全体書き直しの方が早かった

---

## 2026/05/14 (木) - Day 11: 最終チェック + AWS 検証完了の連絡

### やったこと

#### 最終チェック

* Live Demo 動作確認 (PC + モバイル)

  * `https://zhabc001.me` (HTTPS, 訪問者カウンター動作)
  * `https://www.zhabc001.me` (リダイレクト正常)
  * `http://zhabc001.me` → HTTPS 自動リダイレクト
* GitHub リポジトリの公開状態確認 (Public)
* GitHub Actions ステータス確認 (全て緑 ✅)
* README / DEVLOG の最終整理

#### 応募書類の準備

* + 応募エントリーフォーム用の文章作成

  * 制作物 概要・詳細
  * 開発の経緯・ストーリー (建築工学から IT への転職背景)
  * 使用技術と選定理由 (各技術の trade-off も記載)

#### AWS アカウント検証完了の連絡受領

AWS から検証完了の連絡を受領。
ただし、CloudFront 利用権限はバックエンドチームによる
開通作業が進行中とのこと。

**判断**: 応募 (5/15 15:00 締切) 前に CloudFront 移行を
試みることはせず、現状の Cloudflare 構成を維持。

**理由**:

* 時間リスク回避 (移行作業中の Live Demo 停止リスク)
* 安定性優先 (応募作品の信頼性確保)
* "Stability over New Features" の原則
* 応募後の段階的移行 = より実践的な経験

**応募後の計画**:

1. CloudFront 利用権限開通の確認
2. ACM で SSL 証明書を us-east-1 で発行
3. Terraform で CloudFront ディストリビューション定義
4. OAC で S3 を CloudFront 経由のみアクセス可能に
5. DNS 切替え (Cloudflare → CloudFront)
6. 検証 + Cloudflare キャッシュクリア
7. README / DEVLOG への記録

### 学んだこと

#### Risk Management

* "完成"と"安定運用"は別物
* 締切間際の大きな変更はリスクが高い
* "やらない判断"も技術的判断の一つ

#### 段階的な改善計画

* 応募 = 終点ではなく、継続的改善の起点
* 移行プロセス自体も学びになる
* "段階的なリリース" は実運用でも重要


---

## 2026/05/25 (月) - Day 12: AI Assistant UI 追加

### やったこと

* 既存の履歴書ページに `AI Project Assistant` セクションを追加
* ナビゲーションに `AI Assistant` へのリンクを追加
* Bootstrap のデザインに合わせて、以下のクイック質問ボタンを作成
  * Project Overview
  * AWS Architecture
  * Technical Challenges
  * Cost & Security
  * 日本語説明
* Day 1 版として、まずは静的回答を表示するデモを実装
* 本番 API キーをフロントエンドに置かない方針を決定

### 学んだこと

* まず UI プロトタイプを作り、後からバックエンドを接続する進め方
* AI 機能では、見た目の実装よりも API キー管理とコスト制御が重要
* 静的デモでも、ユーザー体験や画面構成を事前に確認できる

### つまずいた点

* HTML 内で `data-answer` と `data-question` の役割が混在し、後続の API 連携時に質問内容が正しく送られない可能性があった

### 改善したこと

* 後続の動的 API 連携に備え、ボタンは `data-question` を使って実際の質問文を渡す設計に変更

---

## 2026/05/26 (火) - Day 13: Mock Lambda API と API Gateway 連携

### やったこと

* AI Assistant 用の Lambda 関数 `ai-assistant-api` を作成
* API Gateway に `POST /ask` ルートを追加
* Lambda から固定レスポンスを返す Mock API を実装
* フロントエンド JavaScript から `/ask` API を呼び出す処理を追加
* PowerShell の `Invoke-RestMethod` で API Gateway 経由の動作確認を実施
* CORS 設定を調整し、ローカル開発環境と本番ドメインからのアクセスを検証

### 学んだこと

* 既存の `/counter` API と同じ API Gateway 上に新しいルートを追加できる
* PowerShell では複数行コマンドの入力方法に注意が必要
* ブラウザで失敗して PowerShell で成功する場合、CORS や Origin の違いを疑うべき
* `file://` で直接 HTML を開くと Origin が `null` になることがある

### つまずいた点

* PowerShell で `Invoke-RestMethod` を途中で改行して実行し、URI の解析エラーが発生
* ローカル表示時に CORS による通信エラーが発生

### 改善したこと

* PowerShell では一行コマンドで API をテスト
* API Gateway / Lambda 側の CORS 設定に `https://zhabc001.me` とローカル開発用 Origin を追加
* フロントエンドでは通信エラー時のメッセージを表示するようにした

---

## 2026/05/27 (水) - Day 14: Gemini API 連携

### やったこと

* Gemini API キーを取得し、Lambda の環境変数 `GEMINI_API_KEY` として設定
* フロントエンドから直接 Gemini API を呼び出さず、API Gateway + Lambda 経由で呼び出す構成にした
* Python 標準ライブラリ `urllib` を使って Gemini API の `generateContent` を呼び出し
* 入力文字数を 500 文字以内に制限
* 出力トークン数を制限し、API コストを抑える設定を追加
* 日本語・英語・中国語の質問に対応するプロンプトを作成
* `このプロジェクト` が Cloud Resume Challenge を指すようにプロンプトを調整

### 学んだこと

* API キーはフロントエンドではなく、Lambda の環境変数で管理するべき
* AI Assistant では、回答範囲を狭くしすぎると正常な質問まで拒否される
* Prompt Engineering では、`このプロジェクト` のような曖昧な表現も明示的に定義する必要がある
* Lambda コンソールのテストとブラウザからの実行では、入力内容や Origin が異なるため挙動が変わることがある

### つまずいた点

* Gemini が「日本語でこのプロジェクトを説明してください」を無関係な質問と誤判定
* フロントエンドのボタンから送信される内容が `日本語説明` のような短いラベルになっていた
* Python のインデントミスにより `unexpected indent` が発生

### 改善したこと

* ボタンには表示ラベルではなく、`data-question` に具体的な質問文を設定
* JavaScript 側で `data-question` がない場合は警告を出すよう変更
* `call_gemini()` 関数内の `prompt` と `payload` のインデントを修正
* Lambda のタイムアウトとメモリ設定を見直し、初回実行時の安定性を改善

---

## 2026/05/28 (木) - Day 15: DynamoDB ログ + 利用上の注意 + ドキュメント更新

### やったこと

* AI Assistant のリクエストログ用 DynamoDB テーブルを追加
* Lambda 実行時に以下のリクエストメタデータを記録
  * Request ID
  * アクセス時刻
  * ハッシュ化された IP アドレス
  * User-Agent
  * 質問文字数
  * リクエスト状態
  * TTL による有効期限
* IP アドレスはそのまま保存せず、ソルト付きハッシュとして保存
* 質問本文はログに保存しない方針にした
* DynamoDB TTL を設定し、一定期間後にログを自動削除する設計にした
* Web ページに AI Assistant の利用上の注意を追加
* README.md と DEVLOG.md を AI Assistant 追加に合わせて更新

### 学んだこと

* AI 機能では、モデル呼び出しだけでなく不正利用防止とコスト管理が重要
* IP アドレスを直接保存せず、ハッシュ化することでプライバシーに配慮できる
* 質問本文を保存しないことで、利用者が誤って個人情報を入力した場合のリスクを下げられる
* DynamoDB TTL を使うことで、ログを一定期間後に自動削除できる
* S3 直接アクセスと独自ドメイン経由では Origin が異なるため、CORS の挙動も変わる

### つまずいた点

* S3 直接アクセスでは訪問者数が `N/A` になることがあった
  * 原因: 正式ドメイン以外の Origin が CORS で許可されていなかった
  * 判断: ユーザーには独自ドメイン経由でアクセスしてもらう設計のため、正式ドメインを優先
* 初回アクセス直後に AI Assistant が一時的に `APIエラー` を返すことがあった
  * 原因候補: Lambda cold start、Gemini API 応答待ち、タイムアウト設定
  * 改善: Lambda の timeout と memory を調整

### SRE / セキュリティ観点での価値

* フロントエンドに API キーを公開しない設計
* リクエストログによる不正利用検知の土台
* 入力文字数と出力トークン数の制限によるコスト制御
* TTL によるログライフサイクル管理
* 個人情報を保存しない最小限ログ設計

### 今後の改善点

* IP ハッシュ + 日付による日次リクエスト制限
* DynamoDB による回答キャッシュ
* CloudWatch Alarm による異常な API 呼び出し検知
* Cloudflare Turnstile による bot 対策
* AI Assistant 関連リソースの Terraform 管理への統合

---

## AI Assistant 拡張の振り返り

### 追加した成果物

* Web サイト上の AI Project Assistant セクション
* API Gateway `POST /ask`
* Lambda `ai-assistant-api`
* Gemini API 連携
* DynamoDB リクエストログ
* 利用上の注意表示
* README / DEVLOG の更新

### 特に意識した点

**セキュリティ**:

* Gemini API キーをフロントエンドに置かない
* API キーは Lambda 環境変数で管理
* CORS を本番ドメイン中心に制限
* 質問本文と生 IP アドレスを保存しない

**コスト管理**:

* 低コストモデルを使用
* 入力文字数を 500 文字以内に制限
* 出力トークン数を制限
* ログを TTL で自動削除
* 今後はキャッシュと日次リクエスト制限を追加予定

**運用性**:

* PowerShell、Lambda コンソール、ブラウザの 3 つの経路で動作確認
* CloudWatch Logs によるエラー確認
* Mock API → Gemini API → ログ追加という段階的リリース

### 面接で説明できるポイント

* AI 機能を単に追加しただけでなく、API キー管理、CORS、ログ、コスト管理まで考慮した
* Serverless 構成で既存の Cloud Resume Challenge を拡張した
* フロントエンド、API Gateway、Lambda、Gemini API、DynamoDB の end-to-end 構成を実装した
* Privacy by Design の考え方に基づき、保存するログを最小限にした

---

## プロジェクト全体の振り返り (5/2 - 5/14)

### 開発期間

13 日間 (応募締切までの実質時間)

### 完成した成果物

#### フロントエンド

* HTML/CSS/JavaScript による履歴書ページ (Bootstrap ベース)
* 訪問者カウンター表示機能 (fetch API + CORS)

#### バックエンド

* Lambda Function (Python 3.12)
* DynamoDB Atomic Counter
* API Gateway HTTP API
* AI Assistant 用 Lambda + Gemini API 連携

#### インフラ

* S3 静的ウェブサイトホスティング
* Cloudflare 経由 HTTPS + CDN + DDoS 防護
* カスタムドメイン (zhabc001.me)
* 17 個の AWS リソース全て Terraform IaC 管理

#### 監視・運用

* CloudWatch Logs (Lambda 実行ログ, 7 日保持)
* CloudWatch Alarm (Errors > 0 監視 + SNS メール通知)
* IAM 最小権限ポリシー
* AI Assistant のリクエストメタデータ記録
* DynamoDB TTL によるログ自動削除

#### テスト・CI/CD

* pytest + moto による単体テスト (5 ケース)
* GitHub Actions による push 時自動テスト実行

#### 運用コスト

* 月額 0 円 (AWS Always Free Tier + Cloudflare Free Plan)

### 主な学び

**技術面**:

* AWS の主要サービス連携 (S3, Lambda, DynamoDB, API Gateway, IAM, CloudWatch)
* HTTP プロトコル、CORS、JSON データ形式
* Python + boto3 によるサーバーレス開発
* Terraform による IaC 実践 (terraform import 含む)
* pytest + GitHub Actions による CI/CD
* Cloudflare による HTTPS 化と CDN
* Gemini API を利用した AI Assistant 実装

**SRE 観点**:

* 可観測性 (Observability) の実装
* 最小権限の原則 (Principle of Least Privilege)
* コスト最適化 (Always Free Tier の活用)
* Alert Fatigue 対策
* Shift-left のテスト戦略
* Infrastructure as Code
* Risk Management (締切前の変更回避)
* AI API の安全なバックエンド連携
* プライバシーに配慮したログ設計

**ソフトスキル**:

* 計画的な開発 (13 日間で完了)
* 予期しない問題 (CloudFront 検証待ち) への対応
* 代替案 (Cloudflare) を検討する柔軟性
* 継続的なドキュメンテーション (DEVLOG, README)
* "やらない判断"の重要性

### 応募後の改善計画

**短期 (1 ヶ月以内)**:

* AI Assistant の回答キャッシュ追加
* IP ハッシュ + 日付による簡易レート制限
* AI Assistant 関連リソースの Terraform 管理
* CloudFront による AWS ネイティブ HTTPS 化
* API Gateway を含めた完全な Terraform IaC 管理
* pytest-cov によるカバレッジ計測
* Qiita / Zenn での技術記事執筆

**中期 (3-6 ヶ月)**:

* 構造化ログ (logging モジュール) への移行
* X-Ray による分散トレーシング
* AWS WAF によるセキュリティ強化
* `terraform.tfstate` を S3 backend で管理
* 複数環境 (dev/staging/prod) 対応

### 終わりに

このプロジェクトを通じて、AWS の知識を実践に移し、
SRE エンジニアとして必要な
「考える力」「決断力」「継続的改善の姿勢」を養うことができました。

特に、CloudFront 検証待ちという予期しない課題に対し、
Cloudflare による代替実装を選択した経験は、
"完璧な解決策"よりも"現実的な解決策"を選ぶ重要性を学ばせてくれました。

応募作品としての提出だけでなく、これからも継続的に改善し、
業務でも応用できる実用的なポートフォリオとして育てていきます。

