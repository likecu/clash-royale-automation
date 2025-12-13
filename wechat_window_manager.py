#!/usr/bin/env python3
"""
将微信窗口置顶并调整大小
"""

import os
import sys
import subprocess

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cr.screenshot import ScreenshotManager

def main():
    """主函数"""
    print("=== 微信窗口管理工具 ===")
    
    # 获取当前微信窗口状态
    print("\n1. 获取当前微信窗口状态...")
    current_pos = subprocess.run(["osascript", "-e", 'tell application "System Events"', '-e', 'tell process "WeChat"', '-e', 'get position of window 1', '-e', 'end tell', '-e', 'end tell'], capture_output=True, text=True).stdout.strip()
    current_size = subprocess.run(["osascript", "-e", 'tell application "System Events"', '-e', 'tell process "WeChat"', '-e', 'get size of window 1', '-e', 'end tell', '-e', 'end tell'], capture_output=True, text=True).stdout.strip()
    
    print(f"   当前位置: {current_pos}")
    print(f"   当前大小: {current_size}")
    
    # 计算3/4大小
    if current_size:
        try:
            width, height = map(int, current_size.replace(',', '').split())
            scaled_width = int(width * 0.75)
            scaled_height = int(height * 0.75)
            print(f"   3/4缩放后: ({scaled_width}, {scaled_height})")
        except ValueError:
            print("   无法计算缩放大小")
    
    # 创建截图管理器实例
    sm = ScreenshotManager()
    
    # 将微信窗口置顶
    print("\n2. 将微信窗口置顶...")
    success = sm.bring_wechat_to_front()
    
    if success:
        print("✓ 微信窗口已成功置顶")
    else:
        print("✗ 无法将微信窗口置顶")
        return
    
    # 调整窗口大小为当前的3/4
    print("\n3. 调整微信窗口大小为当前的3/4...")
    
    # 获取当前窗口大小
    current_size_output = subprocess.run(["osascript", "-e", 'tell application "System Events"', '-e', 'tell process "WeChat"', '-e', 'get size of window 1', '-e', 'end tell', '-e', 'end tell'], capture_output=True, text=True).stdout.strip()
    
    if current_size_output:
        try:
            width, height = map(int, current_size_output.replace(',', '').split())
            scaled_width = int(width * 0.75)
            scaled_height = int(height * 0.75)
            
            # 使用AppleScript调整窗口大小
            applescript = f'''tell application "System Events"
    tell process "WeChat"
        set size of window 1 to {{ {scaled_width}, {scaled_height} }}
    end tell
end tell'''
            
            result = subprocess.run(["osascript", "-e", applescript], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✓ 成功将微信窗口大小调整为: ({scaled_width}, {scaled_height})")
            else:
                print(f"⚠ 调整窗口大小失败: {result.stderr}")
        except ValueError:
            print("✗ 无法解析当前窗口大小")
    
    # 再次获取调整后的窗口状态
    print("\n4. 调整后的微信窗口状态...")
    new_pos = subprocess.run(["osascript", "-e", 'tell application "System Events"', '-e', 'tell process "WeChat"', '-e', 'get position of window 1', '-e', 'end tell', '-e', 'end tell'], capture_output=True, text=True).stdout.strip()
    new_size = subprocess.run(["osascript", "-e", 'tell application "System Events"', '-e', 'tell process "WeChat"', '-e', 'get size of window 1', '-e', 'end tell', '-e', 'end tell'], capture_output=True, text=True).stdout.strip()
    
    print(f"   新位置: {new_pos}")
    print(f"   新大小: {new_size}")
    
    print("\n=== 操作完成 ===")

if __name__ == "__main__":
    main()
