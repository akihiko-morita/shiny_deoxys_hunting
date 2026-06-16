import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 【設定項目】あなたの環境に合わせて書き換えてください
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SMTP_SERVER = "smtp.gmail.com"        # Gmailのサーバー（そのままでOK）
SMTP_PORT = 587                       # TLS通信のポート（そのままでOK）

# 送信元の設定
SENDER_EMAIL = "sender@gmail.com"  # 送信側(アプリ側)のGmailアドレス
SENDER_PASSWORD = "xxxx xxxx xxxx xxxx" # 手順1で取得した16桁のアプリパスワード

# 送信先の設定（スマホで気付きやすいアドレスがおすすめ）
TO_EMAIL = "your@gmail.com"  # 通知を受け取りたいメールアドレス

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# メール作成と送信処理
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def send_test_email():
    # 1. メールの内容を作成
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = TO_EMAIL
    msg['Subject'] = "【テスト】デオキシス自動厳選システム" # 件名

    # 本文
    body = "これは自動厳選マクロからの通知テストです。\nこのメールが届いていれば、通知機能の連携は成功しています！"
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    try:
        print("➔ メールサーバーに接続中...")
        # 2. SMTPサーバーに接続（安全な通信を開始）
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls() 
        
        # 3. ログイン
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        # 4. メール送信
        print("➔ メールを送信しています...")
        server.send_message(msg)
        
        # 5. 終了
        server.quit()
        print("✨ メール送信に成功しました！受信ボックスを確認してください。")

    except Exception as e:
        print(f"❌ メールの送信に失敗しました: {e}")

# テスト実行
if __name__ == "__main__":
    send_test_email()