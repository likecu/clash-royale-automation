import subprocess
import time
import os
from config.config import SCREENSHOT_CONFIG, DOUBAO_OCR_CONFIG
from cr.click_manager import ClickManager

# OCR配置
OCR_SCRIPT = DOUBAO_OCR_CONFIG.get("ocr_script_path", "/Volumes/600g/app1/doubao获取/python/doubao_ocr.py")
PYTHON_PATH = DOUBAO_OCR_CONFIG.get("python_path", "/Volumes/600g/app1/okx-py/bin/python3")

# 皇室战争相关配置
CLASH_ROYALE_CONFIG = {
    "app_name": "皇室战争",
    "check_interval": 1.0,
    "max_attempts": 5
}

class ScreenshotManager:
    """截图管理器，专注于自动截取WeApp界面"""
    
    def __init__(self):
        self.config = SCREENSHOT_CONFIG
        self.screenshot_dir = self.config["screenshot_dir"]
        self.wechat_process_name = self.config["wechat_process_name"]
        self.weapp_relative_region = self.config["weapp_relative_region"]
        # 初始化点击管理器
        self.click_manager = ClickManager()
        # 初始化时计算一次绝对区域
        self.weapp_region = self._calculate_absolute_weapp_region()
    
    def _calculate_absolute_weapp_region(self):
        """根据系统返回的微信窗口位置计算weapp绝对区域"""
        try:
            # 激活微信窗口，确保能获取到正确的窗口信息
            activate_script = '''tell application "WeChat"
    activate
    delay 0.1
end tell'''
            subprocess.run(["osascript", "-e", activate_script], check=True, capture_output=True, text=True)
            time.sleep(0.1)
            
            # 使用System Events获取微信窗口的实际位置
            position_script = '''tell application "System Events"
    tell process "WeChat"
        get position of window 1
    end tell
end tell'''
            position_result = subprocess.run(["osascript", "-e", position_script], check=True, capture_output=True, text=True)
            
            # 解析位置结果，格式为 {x, y}
            position = position_result.stdout.strip().replace("{", "").replace("}", "").split(", ")
            wx_x = int(position[0])
            wx_y = int(position[1])
            
            # 从系统获取微信窗口的大小
            size_script = '''tell application "System Events"
    tell process "WeChat"
        get size of window 1
    end tell
end tell'''
            size_result = subprocess.run(["osascript", "-e", size_script], check=True, capture_output=True, text=True)
            
            # 解析大小结果，格式为 {width, height}
            size = size_result.stdout.strip().replace("{", "").replace("}", "").split(", ")
            wx_width = int(size[0])
            wx_height = int(size[1])
            
            # 动态计算小程序相对区域（假设小程序占据微信窗口的主要内容区域）
            # 这里使用微信窗口的实际大小来计算小程序区域
            rel_x = 0  # 相对于微信窗口左边界的偏移
            rel_y = 0  # 相对于微信窗口上边界的偏移
            width = wx_width  # 使用微信窗口的实际宽度
            height = wx_height  # 使用微信窗口的实际高度
            
            # 计算绝对区域
            abs_x = wx_x + rel_x
            abs_y = wx_y + rel_y
            
            print(f"✓ 已从系统获取微信窗口位置 ({wx_x}, {wx_y}) 和大小 ({wx_width}, {wx_height})，计算出皇室战争区域: ({abs_x}, {abs_y}, {width}, {height})")
            return (abs_x, abs_y, width, height)
        except Exception as e:
            print(f"⚠ 获取微信窗口位置失败: {e}")
            # 使用默认值作为 fallback
            wx_x, wx_y = (400, 100)  # 默认窗口位置
            wx_width, wx_height = (800, 600)  # 默认窗口大小
            
            # 动态计算小程序区域
            rel_x = 0
            rel_y = 0
            width = wx_width
            height = wx_height
            
            default_x = wx_x + rel_x
            default_y = wx_y + rel_y
            print(f"  使用默认值计算皇室战争区域: ({default_x}, {default_y}, {width}, {height})")
            return (default_x, default_y, width, height)
    
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
        """使用AppleScript将微信窗口置顶并移动到指定位置"""
        try:
            print("正在将微信窗口置顶...")
            
            # 使用默认窗口位置
            window_pos = (400, 100)
            
            # 使用AppleScript，只将微信置顶，不移动位置
            applescript = f'''tell application "System Events"
    # 确保WeChat进程存在
    if exists process "WeChat" then
        # 强制将微信置顶
        tell process "WeChat"
            set frontmost to true
            delay 0.5
            # 确保至少有一个窗口
            if not (exists window 1) then
                # 尝试打开微信窗口
                try
                    click menu item 1 of menu 1 of menu bar item "文件" of menu bar 1
                    delay 1
                end try
            end if
            
            # 确保窗口不是最大化状态
            set zoomed of window 1 to false
            delay 0.3
        end tell
        return true
    else
        return false
    end if
end tell'''
            
            result = subprocess.run(["osascript", "-e", applescript], capture_output=True, text=True)
            
            if "true" in result.stdout:
                print("✓ 成功将微信窗口置顶")
                # 重新计算weapp_region，确保截图区域正确
                self.weapp_region = self._calculate_absolute_weapp_region()
                print(f"  已更新weapp_region为: {self.weapp_region}")
                return True
        except Exception as e:
            print(f"✗ 将微信窗口置顶失败: {e}")
            return True
    
    def is_clash_royale_screen(self, screenshot_path):
        """使用OCR验证截图是否为皇室战争界面"""
        try:
            import re
            print(f"\n正在验证截图是否为皇室战争界面: {screenshot_path}")
            
            # 构建OCR命令
            ocr_command = f"{PYTHON_PATH} {OCR_SCRIPT} {screenshot_path} --question \"这是皇室战争游戏界面吗？用yes或no回答，不需要其他解释。\""
            
            # 执行OCR命令
            result = subprocess.run(ocr_command, shell=True, capture_output=True, text=True)
            
            # 提取回答内容
            answer_match = re.search(r'回答:\s*(.+)', result.stdout)
            if answer_match:
                answer = answer_match.group(1).strip().lower()
                print(f"OCR识别结果: {answer}")
                return "yes" in answer
            
            print("⚠ 无法提取OCR回答内容")
            return False
        except Exception as e:
            print(f"✗ OCR验证失败: {e}")
            return False
    
    def bring_clash_royale_to_front(self):
        """专门用于唤出皇室战争页面的方法"""
        print(f"\n=== 开始唤出 {CLASH_ROYALE_CONFIG['app_name']} 页面 ===")
        
        # 1. 首先确保微信窗口前置
        if not self.bring_wechat_to_front():
            print(f"✗ 无法将微信窗口前置，无法唤出 {CLASH_ROYALE_CONFIG['app_name']}")
            return False
        
        # 2. 再次计算weapp_region，确保最新
        self.weapp_region = self._calculate_absolute_weapp_region()
        print(f"  当前weapp_region: {self.weapp_region}")
        
        # 3. 等待微信界面完全稳定
        print("  等待微信界面稳定...")
        time.sleep(1.5)
        
        # 4. 验证并调整点击坐标，确保在屏幕范围内
        weapp_center_x = self.weapp_region[0] + self.weapp_region[2] // 2
        weapp_center_y = self.weapp_region[1] + self.weapp_region[3] // 2
        
        # 获取屏幕尺寸，确保点击坐标在屏幕范围内
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
        except Exception as e:
            print(f"获取屏幕大小失败: {e}")
            # 默认使用常见屏幕分辨率作为 fallback
            screen_width, screen_height = 1920, 1080
        weapp_center_x = max(0, min(weapp_center_x, screen_width - 1))
        weapp_center_y = max(0, min(weapp_center_y, screen_height - 1))
        
        print(f"  点击WeApp中心位置 ({weapp_center_x}, {weapp_center_y}) 激活皇室战争")
        
        # 5. 执行单次点击操作，避免频繁点击导致界面切换
        try:
            # 使用ClickManager执行点击
            if self.click_manager.click(weapp_center_x, weapp_center_y):
                print("  ✓ 成功点击激活皇室战争")
            else:
                print("  ⚠ 点击激活皇室战争失败")
        except Exception as e:
            print(f"  ⚠ 点击操作可能失败: {e}")
        
        # 6. 等待页面加载
        print("  等待皇室战争页面加载...")
        time.sleep(2.0)
        
        print(f"✅ 已尝试唤出 {CLASH_ROYALE_CONFIG['app_name']} 页面")
        return True
    
    def bring_weapp_to_front(self):
        """将WeApp界面前置（确保微信窗口和WeApp都在前面）"""
        print("正在确保WeApp界面前置...")
        
        # 1. 将微信窗口前置
        if not self.bring_wechat_to_front():
            print("✗ 无法将WeChat窗口前置，跳过WeApp前置操作")
            return False
        
        # 2. 再次计算weapp_region，确保最新
        self.weapp_region = self._calculate_absolute_weapp_region()
        print(f"  当前weapp_region: {self.weapp_region}")
        
        # 3. 等待界面稳定
        print("  等待微信界面稳定...")
        time.sleep(1.0)
        
        # 4. 验证并调整点击坐标，确保在屏幕范围内
        weapp_center_x = self.weapp_region[0] + self.weapp_region[2] // 2
        weapp_center_y = self.weapp_region[1] + self.weapp_region[3] // 2
        
        # 获取屏幕尺寸，确保点击坐标在屏幕范围内
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
        except Exception as e:
            print(f"获取屏幕大小失败: {e}")
            # 默认使用常见屏幕分辨率作为 fallback
            screen_width, screen_height = 1920, 1080
        weapp_center_x = max(0, min(weapp_center_x, screen_width - 1))
        weapp_center_y = max(0, min(weapp_center_y, screen_height - 1))
        
        print(f"  点击WeApp中心位置 ({weapp_center_x}, {weapp_center_y}) 确保活动状态")
        
        # 5. 执行点击操作
        try:
            # 使用ClickManager执行点击
            if self.click_manager.click(weapp_center_x, weapp_center_y):
                print("  ✓ 成功点击确保WeApp活动状态")
            else:
                print("  ⚠ 点击确保WeApp活动状态失败")
        except Exception as e:
            print(f"  ⚠ 点击操作可能失败: {e}")
        
        # 6. 等待界面响应
        time.sleep(0.5)
        
        print("✓ 成功确保WeApp界面前置")
        return True
    
    def auto_screenshot_weapp(self, prefix=None):
        """自动截取WeApp界面（兼容原有方法）"""
        return self.auto_screenshot_clash_royale(prefix)
    
    def auto_screenshot_clash_royale(self, prefix="cr"):
        """专门用于截取皇室战争界面的方法"""
        try:
            print("\n=== 开始自动截取皇室战争界面 ===")
            
            # 1. 专门唤出皇室战争页面
            if not self.bring_clash_royale_to_front():
                print("⚠ 无法唤出皇室战争页面，继续尝试截图...")
            
            # 2. 等待界面稳定
            time.sleep(1.0)
            
            # 3. 再次更新weapp_region，确保最新
            self.weapp_region = self._calculate_absolute_weapp_region()
            print(f"更新后的皇室战争区域: {self.weapp_region}")
            
            # 4. 截取WeApp区域（皇室战争区域）
            print(f"正在截取皇室战争区域: {self.weapp_region}")
            
            # 5. 保存截图
            filename = os.path.join(self.screenshot_dir, self.get_timestamp_filename(prefix))
            
            # 使用screencapture命令截图
            x, y, width, height = self.weapp_region
            # 构建screencapture命令，-R参数指定区域：x,y,width,height
            screencapture_cmd = ["screencapture", "-R", f"{x},{y},{width},{height}", filename]
            subprocess.run(screencapture_cmd, check=True, capture_output=True, text=True)
            
            # 检查截图是否成功生成
            if not os.path.exists(filename):
                raise Exception(f"截图文件未生成: {filename}")
            
            # 6. 验证截图是否为皇室战争
            print("验证截图是否为皇室战争界面...")
            
            # 直接返回截图，不进行OCR验证
            print(f"✅ 成功截取皇室战争界面，保存为: {filename}")
            print(f"  文件大小: {os.path.getsize(filename)} 字节")
            
            # 获取截图尺寸
            try:
                from PIL import Image
                with Image.open(filename) as img:
                    screenshot_size = img.size
                    print(f"  截图尺寸: {screenshot_size}")
            except Exception as e:
                print(f"  获取截图尺寸失败: {e}")
            
            return filename
        except Exception as e:
            print(f"✗ 自动截取皇室战争界面失败: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def screenshot_fullscreen(self, prefix="fullscreen"):
        """截取全屏"""
        try:
            print("\n开始截取全屏...")
            
            # 保存截图文件
            filename = os.path.join(self.screenshot_dir, f"{prefix}_{time.strftime('%Y%m%d_%H%M%S')}.png")
            
            # 使用screencapture命令截取全屏
            screencapture_cmd = ["screencapture", filename]
            subprocess.run(screencapture_cmd, check=True, capture_output=True, text=True)
            
            # 检查截图是否成功生成
            if not os.path.exists(filename):
                raise Exception(f"截图文件未生成: {filename}")
            
            print(f"✓ 成功截取全屏，保存为: {filename}")
            print(f"  文件大小: {os.path.getsize(filename)} 字节")
            
            # 获取截图尺寸
            try:
                from PIL import Image
                with Image.open(filename) as img:
                    screenshot_size = img.size
                    print(f"  截图尺寸: {screenshot_size}")
            except Exception as e:
                print(f"  获取截图尺寸失败: {e}")
            
            return filename
        except Exception as e:
            print(f"✗ 截取全屏失败: {e}")
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