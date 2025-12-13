import time
import os
import subprocess

# 创建截图目录
if not os.path.exists('force_wechat_png'):
    os.makedirs('force_wechat_png')

# 1. 强制激活微信并显示窗口
print("正在强制激活微信并显示窗口...")
# 使用更强大的AppleScript确保微信窗口可见
applescript = '''tell application "WeChat"
    activate
    delay 1
    set visible of window 1 to true
    set bounds of window 1 to {0, 0, 1920, 1080}
    delay 2
end tell'''

# 运行AppleScript
# result = subprocess.run(["osascript", "-e", applescript], capture_output=True, text=True)
# if result.returncode != 0:
#     print(f"⚠ AppleScript执行失败: {result.stderr}")
#     # 尝试另一种方法
#     print("尝试使用另一种方法激活微信...")
#     applescript = '''tell application "System Events"
#     tell process "WeChat"
#         set frontmost to true
#         delay 1
#         if not (exists window 1) then
#             -- 如果没有窗口，尝试点击微信图标
#             click menu item 1 of menu 1 of menu bar item "文件" of menu bar 1
#             delay 1
#         end if
#         set visible of window 1 to true
#         set position of window 1 to {0, 0}
#         set size of window 1 to {1920, 1080}
#     end tell
# end tell'''
#     result = subprocess.run(["osascript", "-e", applescript], capture_output=True, text=True)
#     if result.returncode != 0:
#         print(f"⚠ 第二种方法也失败: {result.stderr}")

# 2. 等待微信窗口显示
time.sleep(3)

# 3. 截取全屏
# timestamp = time.strftime("%Y%m%d_%H%M%S")
# filename = f'force_wechat_png/wechat_force_activated_{timestamp}.png'
# print(f"正在截取全屏，保存为: {filename}")
# screenshot = screencapture命令截取
# screenshot.save(filename)
# print(f"✓ 成功截取全屏")

# # 4. 使用OCR识别微信内容
# print("\n正在使用OCR识别微信内容...")
# ocr_command = f"/Volumes/600g/app1/okx-py/bin/python3 /Volumes/600g/app1/doubao获取/python/doubao_ocr.py {filename} --question \"图里有微信窗口吗？微信窗口里显示的是什么内容？有没有皇室战争游戏界面？\""
# result = subprocess.run(ocr_command, shell=True, capture_output=True, text=True)
# print("\n=== OCR识别结果 ===")
# print(result.stdout)
# if result.stderr:
#     print("\n=== OCR错误信息 ===")
#     print(result.stderr)
