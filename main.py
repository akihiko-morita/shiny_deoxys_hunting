import pyautogui
import random
import serial
import smtplib
import time
import winsound

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 【メール通知の設定】お使いの環境に合わせて書き換えてください
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SMTP_SERVER = "smtp.gmail.com"        # Gmailのサーバー（そのままでOK）
SMTP_PORT = 587                       # TLS通信のポート（そのままでOK）

# 送信元の設定
SENDER_EMAIL = "sender@gmail.com"  # 送信側(アプリ側)のGmailアドレス
SENDER_PASSWORD = "xxxx xxxx xxxx xxxx" # 手順1で取得した16桁のアプリパスワード

# 送信先の設定（スマホで気付きやすいアドレスがおすすめ）
TO_EMAIL = "your@gmail.com"  # 通知を受け取りたいメールアドレス

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 【固定設定】ターゲットの座標と通常色のRGB
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TARGET_X = 1343
TARGET_Y = 152
NORMAL_R, NORMAL_G, NORMAL_B = 254, 132, 73

THRESHOLD = 5      # 色の許容誤差
TIMEOUT_SEC = 40   # 色違いとみなすタイムアウト時間（秒）

TODAY_STR = time.strftime("%Y-%m-%d", time.localtime())
LOG_FILE_PATH = f"deoxys_hunt_{TODAY_STR}.log"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 各種関数定義
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def check_screen():
    """通常色判定を同時に行う関数"""
    screenshot = pyautogui.screenshot()
    
    # デオキシスの色チェック
    deoxys_color = screenshot.getpixel((TARGET_X, TARGET_Y))
    is_normal = (abs(deoxys_color[0] - NORMAL_R) <= THRESHOLD and
                 abs(deoxys_color[1] - NORMAL_G) <= THRESHOLD and
                 abs(deoxys_color[2] - NORMAL_B) <= THRESHOLD)

    return is_normal

def send_notification(count):
    """色違い出現時にメールを送信する関数"""
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = TO_EMAIL
    msg['Subject'] = "✨✨【速報】色違いデオキシスが出現しました！ ✨✨"

    body = f"自動厳選マクロからの通知です。\n\n第 {count} 回目の周回にて、色違いデオキシスを検知しました！\nシステムを安全に停止しています。Switchの画面を確認してください。"
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        log("📩 通知メールの送信に成功しました！")
    except Exception as e:
        log(f"❌ 通知メールの送信に失敗しました: {e}")

def log(message):
    """画面にログを表示し、同時に日付つきファイルにも追記する関数"""
    current_time = time.strftime("%H:%M:%S", time.localtime())
    log_line = (f"[{current_time}] {message}")
    print(log_line)
    with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
        f.write(log_line + "\n")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# メイン処理ループ
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
try:
    ser = serial.Serial('COM7', 9600, timeout=1) #COM番号については各自ポート番号に対応したものを入れる
    time.sleep(2) # マイコンの再起動を待つためのディレイ
    print("マイコンとの接続に成功しました。")
except Exception as e:
    print(f"マイコンの接続に失敗しました: {e}")
    exit()

print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print(" 【ツインシステム】デオキシス自動厳選マクロ (メール通知搭載版)")
print(" 終了するには ターミナルで [Ctrl + C] を押してください。")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

loop_count = 1 #中断した場合はここをいじれば途中からカウントできます

try:
    while True:
        log(f"---- 厳選周回 第 {loop_count} 回目 スタート ---")
        log("デオキシス出現待ちフェーズ開始...")
        
        start_time = time.time()
        is_shiny = False  # 色違いフラグ
        
        while True:
            is_normal = check_screen()
            
            # 通常色デオキシスが目の前に現れたかチェック
            if is_normal:
                log("【通常色を検知】リセットシークエンスへ移行します。")
                break

            # タイムアウト判定
            elapsed_time = time.time() - start_time
            if elapsed_time >= TIMEOUT_SEC:
                log(f"【警告】{TIMEOUT_SEC}秒経過しても通常色が検知されませんでした。")
                is_shiny = True
                break
            
            # 通常時のAボタン送信と待機
            ser.write(b'PRESS_A\n')

            # 待機時間を乱数にする(0.4-1.0秒)
            a_interval = random.choice([0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
            time.sleep(a_interval)

        # 出現待ちループを抜けたあとの分岐
        if is_shiny:
            print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print(" ✨✨✨ 色違いデオキシスが出現しました！ ✨✨✨")
            print(" 🚀 メールを送信し、システムを安全に停止します。")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            
            # 1. バックグラウンドでメール送信を実行
            send_notification(loop_count)
            
            # 2. パソコン本体からビープ音を鳴らす（5回）
            for _ in range(5):
                winsound.Beep(2000, 500)
            break

        # 通常色の場合は同時押しリセット
        log("ソフトを同時押しリセットします...")
        ser.write(b'RESET_GAME\n')

        # 【超重要】リセットしてからタイトル→ゲーム再開までのベースの待機時間
        base_time = 3
        # 乱数にする為の追加時間(0-2秒)
        additional_time = random.choice([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0])
        time.sleep(base_time + additional_time)

        loop_count += 1

except KeyboardInterrupt:
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(" 【ユーザーによりマクロが停止されました】")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")