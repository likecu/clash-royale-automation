import time
import os
import subprocess

# 创建截图目录
if not os.path.exists('debug_png'):
    os.makedirs('debug_png')

# 1. 截取全屏
timestamp = time.strftime("%Y%m%d_%H%M%S")
filename = f'debug_png/fullscreen_debug_{timestamp}.png'
print(f"正在截取全屏，保存为: {filename}")
# 使用screencapture命令截取全屏
subprocess.run(["screencapture", filename], check=True, capture_output=True, text=True)
print(f"✓ 成功截取全屏，文件大小: {os.path.getsize(filename)} 字节")

# 获取截图尺寸
try:
    from PIL import Image
    with Image.open(filename) as img:
        screenshot_size = img.size
        print(f"  截图尺寸: {screenshot_size}")
except Exception as e:
    print(f"  获取截图尺寸失败: {e}")

# 2. 获取当前鼠标位置
try:
    applescript = '''tell application "System Events"
    set mouse_pos to position of mouse
    return mouse_pos
end tell'''
    result = subprocess.run(["osascript", "-e", applescript], check=True, capture_output=True, text=True)
    # 解析结果，格式为 {x, y}
    mouse_pos_str = result.stdout.strip().replace("{", "").replace("}", "").split(", ")
    mouse_pos = (int(mouse_pos_str[0]), int(mouse_pos_str[1]))
    print(f"\n当前鼠标位置: {mouse_pos}")
except Exception as e:
    print(f"\n获取鼠标位置失败: {e}")

# 3. 获取屏幕分辨率
try:
    applescript = '''tell application "Finder"
    set screen_resolution to bounds of window of desktop
    return screen_resolution
end tell'''
    result = subprocess.run(["osascript", "-e", applescript], check=True, capture_output=True, text=True)
    # 解析结果，格式为 {0, 0, width, height}
    bounds = result.stdout.strip().replace("{", "").replace("}", "").split(", ")
    screen_width = int(bounds[2])
    screen_height = int(bounds[3])
    print(f"屏幕分辨率: ({screen_width}, {screen_height})")
except Exception as e:
    print(f"获取屏幕分辨率失败: {e}")
