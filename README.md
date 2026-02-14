# subject_4-2-2_1-1

提出用課題
4-2-2 API連携実践課題
1-1. Google ドライブ API


# Google Drive Upload Tool (OAuth版)

##  概要
PythonからGoogle Driveへファイルをアップロードするツールです。  
Google Workspaceを使用せず、個人のGoogleアカウントでOAuth認証を行い、Driveへファイルをアップロードできます。

---

##  実装した機能

- Google Drive APIを利用したファイルアップロード機能
- OAuth2.0によるユーザー認証
- 認証トークンの保存による再ログイン不要の仕組み
- エラーハンドリング（403 access_denied対応）

---

##  使用技術

- Python 3.x
- Google Drive API
- OAuth 2.0
- google-api-python-client
- google-auth-oauthlib

---

##  セットアップ方法

### ① 必要ライブラリのインストール

`bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`

### ② Google Cloudでの設定

1.Google Cloud Consoleで新規プロジェクト作成
2.Google Drive APIを有効化
3.OAuth同意画面を設定（外部）
4.デスクトップアプリ用OAuthクライアントIDを作成
5.credentials.json をプロジェクトフォルダに配置

### ③ 実行

`bash
python upload_to_drive_oauth.py`

初回実行時にブラウザが開き、Google認証を行います。
認証後、ファイルがGoogle Driveにアップロードされます。
