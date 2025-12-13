import time
import os
import subprocess

# 创建截图目录
if not os.path.exists('wechat_png'):
    os.makedirs('wechat_png')

# 1. 激活微信
print("正在激活微信...")
applescript = '''tell application "WeChat"
    activate
    delay 1
end tell'''
subprocess.run(["osascript", "-e", applescript], check=True, capture_output=True, text=True)

# 2. 等待微信前置
time.sleep(1)

# 3. 截取全屏
# timestamp = time.strftime("%Y%m%d_%H%M%S")
# filename = f'wechat_png/wechat_activated_{timestamp}.png'
# print(f"正在截取全屏，保存为: {filename}")
# 使用screencapture命令截取全屏
# subprocess.run(["screencapture", filename], check=True, capture_output=True, text=True)
# print(f"✓ 成功截取全屏")

# 4. 使用OCR识别微信内容
print("\n正在使用OCR识别微信内容...")
ocr_command = f"/Volumes/600g/app1/okx-py/bin/python3 /Volumes/600g/app1/doubao获取/python/doubao_ocr.py {filename} --question \"图里有微信窗口吗？微信窗口里显示的是什么内容？\""
result = subprocess.run(ocr_command, shell=True, capture_output=True, text=True)
print("\n=== OCR识别结果 ===")
print(result.stdout)
if result.stderr:
    print("\n=== OCR错误信息 ===")
    print(result.stderr)
