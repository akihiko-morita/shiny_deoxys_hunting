import pyautogui
import time
import math

# 🎯 特定したターゲット情報
TARGET_X = 1343
TARGET_Y = 152
NORMAL_R, NORMAL_G, NORMAL_B = 254, 132, 73

# 🎨 判定の「許容誤差」の設定
# 映像の微妙なノイズや処理落ちで1〜2前後数値がズレても反応できるようにします
THRESHOLD = 5 

def is_target_color(current, target, threshold):
    """現在の色がターゲットの色と誤差の範囲内で一致するか判定する関数"""
    return (abs(current[0] - target[0]) <= threshold and
            abs(current[1] - target[1]) <= threshold and
            abs(current[2] - target[2]) <= threshold)

print("━━━━━━━━━━━━━━━━━━━━━━━━━")
print("【通常色デオキシス 判定テスト開始】")
print(f"■ 監視座標: ({TARGET_X}, {TARGET_Y})")
print(f"■ 目標の色 (R,G,B): ({NORMAL_R}, {NORMAL_G}, {NORMAL_B})")
print("1秒おきに判定を行います。終了するには [Ctrl + C] を押してください。")
print("━━━━━━━━━━━━━━━━━━━━━━━━━\n")

try:
    while True:
        # 1. スクショを撮って指定座標の色を取得
        screenshot = pyautogui.screenshot()
        current_color = screenshot.getpixel((TARGET_X, TARGET_Y))
        r, g, b = current_color
        
        current_time = time.strftime("%H:%M:%S", time.localtime())
        
        # 2. 色が通常色のオレンジと一致するか判定
        if is_target_color(current_color, (NORMAL_R, NORMAL_G, NORMAL_B), THRESHOLD):
            print(f"[{current_time}] 色味: ({r:3d}, {g:3d}, {b:3d}) ➔ 🔴【通常デオキシスを検知！！】")
        else:
            print(f"[{current_time}] 色味: ({r:3d}, {g:3d}, {b:3d}) ➔ ⚪️ 通常色ではありません")
            
        # 3. 1秒待機
        time.sleep(1.0)

except KeyboardInterrupt:
    print("\n【テストを終了しました】")