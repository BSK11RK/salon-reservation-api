# Beauty Salon Reservation API

美容院の予約業務を想定して作った、予約管理用のREST APIです。

「ユーザーが予約する」だけではなく、店舗・スタッフ・メニュー・顧客・予約をまとめて管理できるようにし、認証や権限管理まで含めてバックエンド側を実装しました。

FastAPIを中心に、SQLAlchemy・PostgreSQL・Alembic・Docker・pytestを使っています。

## このプロジェクトについて

FastAPIを学習する中で、単純なCRUD APIだけではなく、実際のサービスに近い構成のAPIを作ってみたいと思い、このプロジェクトを作りました。

特に以下の部分を意識しています。

* JWTを使ったログイン認証
* Customer / Staff / Admin のロールごとの権限管理
* SQLAlchemyを使ったテーブル間のリレーション
* 同じスタッフの予約時間が重ならないようにする予約チェック
* Alembicによるデータベースの変更管理
* Docker Composeによる開発環境の構築
* pytestによるAPIの自動テスト

## 主な機能

### ユーザー・認証

ユーザー登録とログインに加えて、JWTによる認証を実装しています。

ユーザーには以下のロールがあります。

```text
customer
staff
admin
```

AdminやStaffを一般ユーザーが自由に作成できないようにし、APIごとにアクセスできるロールを分けています。

### 店舗管理

* 店舗一覧・詳細取得
* 店舗登録
* 店舗更新
* 店舗削除

店舗の管理操作はAdminのみ可能です。

### スタッフ管理

* スタッフ一覧・詳細取得
* スタッフ登録
* スタッフ更新
* スタッフ削除
* Staff自身のプロフィール取得
* Staff自身の担当予約取得

### メニュー管理

* メニュー一覧・詳細取得
* メニュー登録
* メニュー更新
* メニュー削除

メニューの管理操作はAdminのみ可能です。

### 顧客管理

* 顧客一覧・詳細取得
* 顧客登録
* 顧客更新
* 顧客削除
* Customer自身の情報取得

### 予約管理

* 予約作成
* 予約一覧・詳細取得
* 予約更新
* 予約削除
* Customerは自分の予約のみ操作
* Staffは担当予約を取得
* Adminは全予約を管理

## 権限設計

ロールによって操作できる範囲を分けています。

| 操作     | Customer | Staff | Admin |
| ------ | -------- | ----- | ----- |
| ユーザー登録 | ○        | ○     | ○     |
| ユーザー一覧 | ×        | ×     | ○     |
| 店舗閲覧   | ○        | ○     | ○     |
| 店舗管理   | ×        | ×     | ○     |
| メニュー閲覧 | ○        | ○     | ○     |
| メニュー管理 | ×        | ×     | ○     |
| スタッフ管理 | ×        | ×     | ○     |
| 顧客管理   | ×        | ×     | ○     |
| 予約作成   | ○        | ×     | ×     |
| 予約取得   | 自分のみ     | 担当のみ  | 全件    |
| 予約更新   | 自分のみ     | ×     | 全件    |
| 予約削除   | 自分のみ     | ×     | 全件    |

単に「ログインしているか」を確認するだけではなく、ログイン後のユーザーのロールと所有関係も確認するようにしています。

## 予約時間の重複チェック

美容院の予約では、同じスタッフに同じ時間帯の予約を入れられないようにする必要があります。

そのため、予約作成時に既存予約との時間の重複をチェックしています。

```text
existing.start_at < new.end_at
AND
existing.end_at > new.start_at
```

例えば、

```text
10:00 ───── 11:00
      10:30 ───── 11:30
```

は重複するので予約できません。

一方で、

```text
10:00 ───── 11:00
11:00 ───── 12:00
```

のように予約が隣接している場合は登録できます。

## 技術スタック

* Python
* FastAPI
* Pydantic
* SQLAlchemy
* PostgreSQL
* Alembic
* JWT
* pwdlib / Argon2
* pytest
* Docker
* Docker Compose

## ディレクトリ構成

```text
beauty-salon-api/
├── app/
│   ├── models/
│   ├── schemas/
│   ├── routers/
│   ├── services/
│   ├── main.py
│   ├── database.py
│   └── security.py
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── tests/
│   ├── conftest.py
│   ├── test_users.py
│   ├── test_auth.py
│   ├── test_authorization.py
│   ├── test_salons.py
│   ├── test_menus.py
│   ├── test_staffs.py
│   ├── test_customers.py
│   └── test_reservations.py
│
├── Dockerfile
├── compose.yaml
├── alembic.ini
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 起動方法

Docker Desktopを起動した状態で、以下を実行します。

```bash
docker compose up --build
```

FastAPIとPostgreSQLが起動し、アプリケーションコンテナの起動時にAlembicのMigrationも適用されます。

Swagger UI：

```text
http://localhost:8000/docs
```

停止：

```bash
docker compose down
```

## データベース

PostgreSQLはDockerコンテナで起動しています。

```text
FastAPI
   ↓
SQLAlchemy
   ↓
Psycopg
   ↓
PostgreSQL
```

データベースのテーブル構造はAlembicで管理しています。

Migrationを作成する場合：

```bash
docker compose exec app alembic revision --autogenerate -m "describe your change"
```

Migrationを適用する場合：

```bash
docker compose exec app alembic upgrade head
```

## ER図

```mermaid
erDiagram
    USERS ||--o| CUSTOMERS : has
    USERS ||--o| STAFFS : has

    SALONS ||--o{ STAFFS : employs
    SALONS ||--o{ MENUS : offers

    CUSTOMERS ||--o{ RESERVATIONS : makes
    STAFFS ||--o{ RESERVATIONS : handles
    MENUS ||--o{ RESERVATIONS : uses

    USERS {
        int id PK
        string name
        string email UK
        string password_hash
        string role
        datetime created_at
    }

    CUSTOMERS {
        int id PK
        int user_id FK UK
        string name
    }

    STAFFS {
        int id PK
        int user_id FK UK
        string name
        int salon_id FK
    }

    SALONS {
        int id PK
        string name
        string address
    }

    MENUS {
        int id PK
        string name
        int price
        int duration_minutes
        int salon_id FK
    }

    RESERVATIONS {
        int id PK
        int customer_id FK
        int staff_id FK
        int menu_id FK
        datetime start_at
        datetime end_at
    }
```

## テスト

pytestを使ってAPIテストを実装しています。

現在39件のテストがあり、以下のようなケースを確認しています。

* ユーザー登録
* ログイン
* JWT認証
* Customer / Staff / Adminの権限
* 店舗・メニュー管理
* スタッフ・顧客管理
* 予約の作成・取得・更新・削除
* 他人の予約へのアクセス制御
* 予約時間の重複

テスト実行：

```bash
docker compose exec app pytest -v
```

テスト用には専用のSQLiteデータベースを使用し、開発用のPostgreSQLには影響しない構成にしています。

## セキュリティについて

パスワードは平文では保存せず、Argon2を使ってハッシュ化しています。

認証にはJWTを使用し、APIごとに必要なロールを確認しています。

また、Customerについてはロールだけではなく、自分自身のデータであるかも確認するようにしています。

## このプロジェクトで学んだこと

このプロジェクトでは、FastAPIの基本的なAPI作成だけではなく、バックエンド開発で必要になる以下の部分まで実際に実装しました。

* REST API設計
* Pydanticによるバリデーション
* SQLAlchemy ORM
* テーブル間のリレーション
* JWT認証
* Role-based Authorization
* PostgreSQL
* Alembic Migration
* Docker Compose
* pytestによる自動テスト

特に、予約の時間重複チェックやCustomer / Staff / Adminごとの権限制御を実装することで、単純なCRUDではなく、実際の業務を想定したAPIにすることを意識しました。

## 今後やってみたいこと

今後は必要に応じて、以下のような改善も考えています。

* GitHub ActionsによるCI
* 本番環境へのデプロイ
* RoleのEnum化
* ページネーション
* より詳細な予約可能時間の管理
* APIレスポンスやエラーハンドリングの改善

````