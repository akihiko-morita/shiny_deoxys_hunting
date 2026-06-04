import pyautogui
import time

#【固定設定】ターゲットの座標と通常色のRGB
TARGET_X = 1343
TARGET_Y = 152
NORMAL_R, NORMAL_G, NORMAL_B = 254, 132, 73
THRESHOLD = 5      # 色の許容誤差
TIMEOUT_SEC = 40   # 色違いとみなすタイムアウト時間（秒）

TODAY_STR = time.strftime("%Y-%m-%d", time.localtime())
LOG_FILE_PATH = f"deoxys_hunt_{TODAY_STR}.log"

def is_normal_deoxys():
    """指定座標が通常色デオキシスのオレンジ色か判定する関数"""
    screenshot = pyautogui.screenshot()
    current_color = screenshot.getpixel((TARGET_X, TARGET_Y))
    return (abs(current_color[0] - NORMAL_R) <= THRESHOLD and
            abs(current_color[1] - NORMAL_G) <= THRESHOLD and
            abs(current_color[2] - NORMAL_B) <= THRESHOLD)

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
print(" 【ツインシステム】デオキシス自動厳選マクロ (タイムアウト搭載版)")
print(" 終了するには ターミナルで [Ctrl + C] を押してください。")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

loop_count = 1

try:
    while True:
        print(f"\n--- 厳選周回 第 {loop_count} 回目 スタート ---")
        
        log("デオキシス出現待ちフェーズ開始...（1秒おきにAボタンを送信）")
        
        # 出現待ちを開始した「開始時刻」を記録
        start_time = time.time()
        is_shiny = False  # 色違いフラグ
        
        while True:
            # 【ボード到着後】マイコンへ「Aボタンを押せ」と指示
            # ser.write(b'PRESS_A\n') 
            
            # 通常色デオキシスが目の前に現れたかチェック
            if is_normal_deoxys():
                log("🔴【通常色を検知！】リセットシークエンスへ移行します。")
                break  # 出現待ちループを抜けてリセットへ

            # タイムアウト判定（現在時刻 - 開始時刻 ＝ 経過秒数）
            elapsed_time = time.time() - start_time
            if elapsed_time >= TIMEOUT_SEC:
                log(f"【警告】{TIMEOUT_SEC}秒経過しても通常色が検知されませんでした。")
                is_shiny = True
                break  # 出現待ちループを抜ける（リセットはしない）
                
            time.sleep(0.7) # 0.7秒おきにチェック＆Aボタン

        # 出現待ちループを抜けたあとの分岐
        if is_shiny:
            # 色違いが出現した（または想定外のストップ）場合の処理
            print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print(" ✨✨✨ 色違いデオキシスが出現しました！ ✨✨✨")
            print(" システムを安全に停止します。Switchの画面を確認してください。")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            
            # 💡 ここでWindowsの警告音（BEEP音）を鳴らしたりできる
            import winsound
            for _ in range(10): # ピピッという音を5回鳴らす
                winsound.Beep(2000, 500) # 周波数2000Hz、0.5秒
            break # 外側の無限ループも抜けて、完全にプログラムを終了させる

        # 🔄 通常色の場合はリセット＆再起動フェーズへ
        log("🔄 【ソフトリセット実行】ゲームを終了して再起動します...")
        # 💡 【ボード到着後】マイコンへ「再起動コマンド」を送信
        # ser.write(b'RESET_GAME\n')
        
        load_time = 4
        log(f"ゲーム再起動のロード待ち中（ {load_time} 秒間、待機します）...")
        time.sleep(load_time)
        
        log("➔ ロード完了")
        loop_count += 1

except KeyboardInterrupt:
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(" 【ユーザーによりマクロが停止されました】")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")