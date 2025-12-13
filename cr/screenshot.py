import pyautogui
import subprocess
import time
import os
from config.config import SCREENSHOT_CONFIG

class ScreenshotManager:
    """截图管理器，专注于自动截取WeApp界面"""
    
    def __init__(self):
        self.config = SCREENSHOT_CONFIG
        self.screenshot_dir = self.config["screenshot_dir"]
        self.wechat_process_name = self.config["wechat_process_name"]
        self.weapp_region = self.config["weapp_region"]
    
    def set_screenshot_dir(self, dir_path):
        """设置截图保存目录"""
        self.screenshot_dir = dir_path
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
    
    def get_timestamp_filename(self, prefix=None):
        """生成带时间戳的文件名"""
        if prefix is None:
            prefix = self.config["prefix"]
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{timestamp}.png"
    
    def bring_wechat_to_front(self):
        """将微信窗口前置"""
        try:
            print("正在将微信窗口前置...")
            
            # 使用更简单的AppleScript将微信窗口前置
            applescript = '''tell application "WeChat"
    activate
    delay 0.5
end tell'''
            
            subprocess.run(["osascript", "-e", applescript], check=True, capture_output=True, text=True)
            print("✓ 成功将微信窗口前置")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ 未找到WeChat应用: {e}")
            return False
        except Exception as e:
            print(f"✗ 将微信窗口前置失败: {e}")
            return False
    
    def bring_weapp_to_front(self):
        """将WeApp界面前置（确保微信窗口和WeApp都在前面）"""
        print("正在确保WeApp界面前置...")
        
        # 1. 将微信窗口前置
        if not self.bring_wechat_to_front():
            print("✗ 无法将WeChat窗口前置，跳过WeApp前置操作")
            return False
        
        # 2. 等待一下确保界面稳定
        time.sleep(1)
        
        # 3. 可以在这里添加额外的操作，比如点击WeApp界面的某个位置来确保它处于活动状态
        print("✓ 成功确保WeApp界面前置")
        return True
    
    def auto_screenshot_weapp(self, prefix=None):
        """自动截取WeApp界面"""
        try:
            print("\n开始自动截取WeApp界面...")
            
            # 1. 确保WeApp界面前置
            if not self.bring_weapp_to_front():
                # 如果无法将微信窗口前置，仍然尝试截图
                print("⚠ 继续尝试截图...")
            
            # 2. 等待一下确保界面稳定
            time.sleep(2)
            
            # 3. 截取WeApp区域
            print(f"正在截取WeApp区域: {self.weapp_region}")
            screenshot = pyautogui.screenshot(region=self.weapp_region)
            
            # 4. 保存截图文件
            filename = os.path.join(self.screenshot_dir, self.get_timestamp_filename(prefix))
            screenshot.save(filename)
            
            print(f"✓ 成功截取WeApp界面，保存为: {filename}")
            print(f"  文件大小: {os.path.getsize(filename)} 字节")
            print(f"  截图尺寸: {screenshot.size}")
            
            return filename
        except Exception as e:
            print(f"✗ 自动截取WeApp界面失败: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def batch_screenshot_weapp(self, count=3, interval=5, prefix="weapp_batch"):
        """批量截取WeApp界面"""
        print(f"\n开始批量截取WeApp界面，共{count}次，间隔{interval}秒")
        print("=" * 50)
        
        screenshot_files = []
        
        for i in range(count):
            print(f"\n第{i+1}/{count}次截图")
            screenshot = self.auto_screenshot_weapp(prefix)
            if screenshot:
                screenshot_files.append(screenshot)
            
            # 如果不是最后一次，等待指定的间隔时间
            if i < count - 1:
                print(f"等待{interval}秒后进行下一次截图...")
                time.sleep(interval)
        
        print(f"\n✓ 批量截图完成，共生成{len(screenshot_files)}张截图")
        return screenshot_files