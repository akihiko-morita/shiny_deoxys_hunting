import pyautogui
import time
import serial
import winsound

# マイコンが接続されているCOMポート（環境に合わせて変更してください）
try:
    ser = serial.Serial('COM7', 9600, timeout=1)
    time.sleep(2) # マイコンの再起動を待つためのディレイ
    print("マイコンとの接続に成功しました。")
except Exception as e:
    print(f"マイコンの接続に失敗しました: {e}")
    exit()

#【固定設定】ターゲットの座標と通常色のRGB
TARGET_X = 1343
TARGET_Y = 152
NORMAL_R, NORMAL_G, NORMAL_B = 254, 132, 73

#【固定設定】あらすじヘッダーの座標と通常色のRGB
SYNOPOSIS_X = 1574
SYNOPOSIS_Y = 37
SYNOPOSIS_R, SYNOPOSIS_G, SYNOPOSIS_B = 65, 89, 106

THRESHOLD = 5      # 色の許容誤差
TIMEOUT_SEC = 40   # 色違いとみなすタイムアウト時間（秒）

TODAY_STR = time.strftime("%Y-%m-%d", time.localtime())
LOG_FILE_PATH = f"deoxys_hunt_{TODAY_STR}.log"

def check_screen():
    """1回のキャプチャで、通常色判定とあらすじ判定を同時に行う関数"""
    screenshot = pyautogui.screenshot()
    
    # デオキシスの色チェック
    deoxys_color = screenshot.getpixel((TARGET_X, TARGET_Y))
    is_normal = (abs(deoxys_color[0] - NORMAL_R) <= THRESHOLD and
                 abs(deoxys_color[1] - NORMAL_G) <= THRESHOLD and
                 abs(deoxys_color[2] - NORMAL_B) <= THRESHOLD)
    
    # あらすじ画面チェック
    synopsis_color = screenshot.getpixel((SYNOPOSIS_X, SYNOPOSIS_Y))
    is_syn = (abs(synopsis_color[0] - SYNOPOSIS_R) <= THRESHOLD and
              abs(synopsis_color[1] - SYNOPOSIS_G) <= THRESHOLD and
              abs(synopsis_color[2] - SYNOPOSIS_B) <= THRESHOLD)
              
    return is_normal, is_syn

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
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print(" 【ツインシステム】デオキシス自動厳選マクロ (最適化版)")
print(" 終了するには ターミナルで [Ctrl + C] を押してください。")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

loop_count = 1

try:
    while True:
        log(f"\n--- 厳選周回 第 {loop_count} 回目 スタート ---")
        log("デオキシス出現待ちフェーズ開始...")
        
        start_time = time.time()
        is_shiny = False  # 色違いフラグ
        
        while True:
            # 1回のキャプチャで両方の状態を取得（超高速化）
            is_normal, is_syn = check_screen()

            # 1. あらすじ画面の場合はBを押す（あらすじを早く抜けるためディレイを短くする工夫）
            if is_syn:
                ser.write(b'PRESS_B\n')
                time.sleep(0.3) # あらすじ時は少し早めにボタンを押す
                continue
            
            # 2. 通常色デオキシスが目の前に現れたかチェック
            if is_normal:
                log("🔴【通常色を検知！】リセットシークエンスへ移行します。")
                break

            # 3. タイムアウト判定
            elapsed_time = time.time() - start_time
            if elapsed_time >= TIMEOUT_SEC:
                log(f"【警告】{TIMEOUT_SEC}秒経過しても通常色が検知されませんでした。")
                is_shiny = True
                break
            
            # 通常時のAボタン送信と待機
            ser.write(b'PRESS_A\n')
            
            time.sleep(0.7)

        # 出現待ちループを抜けたあ後の分岐
        if is_shiny:
            print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print(" ✨✨✨ 色違いデオキシスが出現しました！ ✨✨✨")
            print(" システムを安全に停止します。Switchの画面を確認してください。")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            for _ in range(10):
                winsound.Beep(2000, 500)
            break

        # 🔄 通常色の場合は同時押しリセット
        log("ソフトを同時押しリセットします...")
        ser.write(b'RESET_GAME\n')

        # 【超重要】リセットしてからタイトル→ゲーム再開までのロード時間
        # ※手動でリセットしてから動かせるようになるまでの時間を測り、余裕を持って＋2〜3秒長めに設定してください
        load_time = 4  
        log(f"ゲーム再起動のロード待ち中（ {load_time} 秒間、待機します）...")
        time.sleep(load_time)

        loop_count += 1

except KeyboardInterrupt:
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(" 【ユーザーによりマクロが停止されました】")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")