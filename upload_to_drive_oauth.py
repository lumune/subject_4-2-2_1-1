#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Drive API（OAuth認証）を使ってローカルファイルをアップロードするスクリプト
個人の Google アカウント（無料）で使用可能
"""

import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


# ============================================================
# 設定（ここだけ確認・変更）
# ============================================================

# OAuth クライアントIDの JSON
# Google Cloud Console からダウンロードしたもの
CLIENT_SECRET_FILE = "client_secret.json"

# アップロードするローカルファイル
LOCAL_FILE_PATH = "example.jpg"

# アップロード先フォルダID（空 [] ならマイドライブ直下）
PARENT_FOLDER_IDS = []

# Drive API のスコープ
SCOPES = ["https://www.googleapis.com/auth/drive.file"]


def upload_file_to_drive():
    creds = None

    # --- 1. トークンがあれば再利用 ---
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    # --- 2. なければ OAuth 認証 ---
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)

        # トークン保存（次回以降ログイン不要）
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    # --- 3. Drive API クライアント作成 ---
    service = build("drive", "v3", credentials=creds)

    # --- 4. ファイル存在チェック ---
    if not os.path.isfile(LOCAL_FILE_PATH):
        raise FileNotFoundError(f"ファイルが見つかりません: {LOCAL_FILE_PATH}")

    # --- 5. メタデータ ---
    file_metadata = {"name": os.path.basename(LOCAL_FILE_PATH)}
    if PARENT_FOLDER_IDS:
        file_metadata["parents"] = PARENT_FOLDER_IDS

    # --- 6. ファイル本体 ---
    media = MediaFileUpload(
        LOCAL_FILE_PATH,
        resumable=True
    )

    # --- 7. アップロード ---
    print(f"アップロード中: {LOCAL_FILE_PATH}")
    result = (
        service.files()
        .create(
            body=file_metadata,
            media_body=media,
            fields="id, name, webViewLink"
        )
        .execute()
    )

    print("アップロード完了 🎉")
    print(f"ファイル名: {result['name']}")
    print(f"ID: {result['id']}")
    print(f"リンク: {result.get('webViewLink')}")


if __name__ == "__main__":
    upload_file_to_drive()
