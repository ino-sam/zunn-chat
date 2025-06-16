# Zunn-Chat

ずんだもんbotは、Streamlitを使用して構築されたチャットアプリケーションです。
ずんだもんと音声付きでチャットできるアプリです。

## 機能

*   ユーザーとのチャット
*   Geminiモデルによる応答生成
*   Voicevoxによるテキストから音声への変換
*   会話履歴の表示

## ファイル構成

*   `app.py`: アプリケーションのエントリーポイント
*   `components/chat.py`: チャットインターフェース
*   `components/history.py`: 会話履歴
*   `utils/gemini.py`: Geminiモデルの統合
*   `utils/voicevox.py`: Voicevoxの統合

## 注意点

*   Voicevoxをローカルで立ち上げた状態でないと動作しません。

## 環境構築

1.  Pythonをインストールしてください。
2.  必要なライブラリをインストールしてください。

    ```
    pip install -r requirements.txt
    ```
3.  Voicevoxをインストールして起動してください。
4.  Gemini APIキーを設定してください。

## 実行方法

1.  Streamlitアプリケーションを実行してください。

    ```
    streamlit run app.py
    ```
