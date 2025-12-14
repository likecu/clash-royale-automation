import subprocess
import time
import os
from config.config import SCREENSHOT_CONFIG, DOUBAO_OCR_CONFIG
from cr.click_manager import ClickManager
from cr.utils import WeChatUtils, SystemUtils

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
        # 添加缓存机制 - 先初始化缓存属性
        self._wx_window_cache = None
        self._screen_size_cache = None
        self._last_calculated_time = 0
        self._cache_timeout = 5.0  # 缓存超时时间，单位：秒
        self._debug = self.config.get("debug", False)
        # 初始化时计算一次绝对区域 - 后调用计算方法
        self.weapp_region = self._calculate_absolute_weapp_region()
    
    def _get_screen_size(self):
        """获取屏幕尺寸，带缓存机制"""
        if self._screen_size_cache is not None:
            return self._screen_size_cache
            
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
            self._screen_size_cache = (screen_width, screen_height)
            return self._screen_size_cache
        except Exception as e:
            if self._debug:
                print(f"获取屏幕大小失败: {e}")
            # 默认使用常见屏幕分辨率作为 fallback
            self._screen_size_cache = (1920, 1080)
            return self._screen_size_cache
    
    def _calculate_absolute_weapp_region(self, force_recalculate=False):
        """根据系统返回的微信窗口位置计算weapp绝对区域，带缓存机制"""
        # 检查缓存是否有效
        current_time = time.time()
        if not force_recalculate and self._wx_window_cache is not None:
            cached_time, cached_region = self._wx_window_cache
            if current_time - cached_time < self._cache_timeout:
                if self._debug:
                    print(f"✓ 使用缓存的皇室战争区域: {cached_region}")
                return cached_region
        
        try:
            # 获取微信窗口位置和大小，不强制前置窗口
            wx_window = WeChatUtils.get_wechat_window_position()
            wx_x = wx_window["x"]
            wx_y = wx_window["y"]
            wx_width = wx_window["width"]
            wx_height = wx_window["height"]
            
            # 动态计算小程序相对区域（假设小程序占据微信窗口的主要内容区域）
            # 这里使用微信窗口的实际大小来计算小程序区域
            rel_x = 0  # 相对于微信窗口左边界的偏移
            rel_y = 0  # 相对于微信窗口上边界的偏移
            width = wx_width  # 使用微信窗口的实际宽度
            height = wx_height  # 使用微信窗口的实际高度
            
            # 计算绝对区域
            abs_x = wx_x + rel_x
            abs_y = wx_y + rel_y
            region = (abs_x, abs_y, width, height)
            
            # 缓存结果
            self._wx_window_cache = (current_time, region)
            if self._debug:
                print(f"✓ 已从系统获取微信窗口位置 ({wx_x}, {wx_y}) 和大小 ({wx_width}, {wx_height})，计算出皇室战争区域: {region}")
            return region
        except Exception as e:
            if self._debug:
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
            region = (default_x, default_y, width, height)
            if self._debug:
                print(f"  使用默认值计算皇室战争区域: {region}")
            return region
    
    def set_screenshot_dir(self, dir_path):
        """设置截图保存目录"""
        self.screenshot_dir = dir_path
        SystemUtils.ensure_dir_exists(dir_path)
    
    def get_timestamp_filename(self, prefix=None):
        """生成带时间戳的文件名"""
        if prefix is None:
            prefix = self.config["prefix"]
        return SystemUtils.get_timestamp_filename(prefix)
    
    def bring_wechat_to_front(self, force=False):
        """使用AppleScript将微信窗口置顶并移动到指定位置"""
        if self._debug:
            print("正在将微信窗口置顶...")
        
        try:
            # 使用WeChatUtils将微信窗口置顶
            if WeChatUtils.bring_wechat_to_front():
                if self._debug:
                    print("✓ 成功将微信窗口置顶")
                # 重新计算weapp_region，确保截图区域正确
                self.weapp_region = self._calculate_absolute_weapp_region(force_recalculate=force)
                if self._debug:
                    print(f"  已更新weapp_region为: {self.weapp_region}")
                return True
            else:
                if self._debug:
                    print("✗ 无法将微信窗口置顶")
                return False
        except Exception as e:
            if self._debug:
                print(f"✗ 将微信窗口置顶失败: {e}")
            return False
    
    def is_clash_royale_screen(self, screenshot_path):
        """使用OCR验证截图是否为皇室战争界面"""
        if self._debug:
            print(f"\n正在验证截图是否为皇室战争界面: {screenshot_path}")
        
        try:
            import re
            
            # 构建OCR命令
            ocr_command = f"{PYTHON_PATH} {OCR_SCRIPT} {screenshot_path} --question \"这是皇室战争游戏界面吗？用yes或no回答，不需要其他解释。\""
            
            # 执行OCR命令
            result = subprocess.run(ocr_command, shell=True, capture_output=True, text=True)
            
            # 提取回答内容
            answer_match = re.search(r'回答:\s*(.+)', result.stdout)
            if answer_match:
                answer = answer_match.group(1).strip().lower()
                if self._debug:
                    print(f"OCR识别结果: {answer}")
                return "yes" in answer
            
            if self._debug:
                print("⚠ 无法提取OCR回答内容")
            return False
        except Exception as e:
            if self._debug:
                print(f"✗ OCR验证失败: {e}")
            return False
    
    def _get_safe_click_coordinates(self):
        """获取安全的点击坐标，确保在屏幕范围内"""
        weapp_center_x = self.weapp_region[0] + self.weapp_region[2] // 2
        weapp_center_y = self.weapp_region[1] + self.weapp_region[3] // 2
        
        # 使用缓存的屏幕尺寸
        screen_width, screen_height = self._get_screen_size()
        
        # 确保点击坐标在屏幕范围内
        safe_x = max(0, min(weapp_center_x, screen_width - 1))
        safe_y = max(0, min(weapp_center_y, screen_height - 1))
        
        return safe_x, safe_y
    
    def bring_clash_royale_to_front(self):
        """专门用于唤出皇室战争页面的方法"""
        if self._debug:
            print(f"\n=== 开始唤出 {CLASH_ROYALE_CONFIG['app_name']} 页面 ===")
        
        # 1. 首先确保微信窗口前置
        if not self.bring_wechat_to_front():
            if self._debug:
                print(f"✗ 无法将微信窗口前置，无法唤出 {CLASH_ROYALE_CONFIG['app_name']}")
            return False
        
        # 2. 等待微信界面完全稳定 - 减少等待时间
        time.sleep(0.3)
        
        if self._debug:
            print(f"✅ 已尝试唤出 {CLASH_ROYALE_CONFIG['app_name']} 页面")
        return True
    
    def bring_weapp_to_front(self):
        """将WeApp界面前置（确保微信窗口和WeApp都在前面）"""
        if self._debug:
            print("正在确保WeApp界面前置...")
        
        # 1. 将微信窗口前置
        if not self.bring_wechat_to_front():
            if self._debug:
                print("✗ 无法将WeChat窗口前置，跳过WeApp前置操作")
            return False
        
        # 2. 等待界面稳定 - 减少等待时间
        time.sleep(0.2)
        
        if self._debug:
            print("✓ 成功确保WeApp界面前置")
        return True
    
    def auto_screenshot_weapp(self, prefix=None):
        """自动截取WeApp界面（兼容原有方法）"""
        return self.auto_screenshot_clash_royale(prefix)
    
    def auto_screenshot_clash_royale(self, prefix="cr", skip_bring_to_front=False):
        """专门用于截取皇室战争界面的方法"""
        if self._debug:
            print("\n=== 开始自动截取皇室战争界面 ===")
        
        try:
            # 1. 专门唤出皇室战争页面（可选跳过）
            if not skip_bring_to_front:
                if not self.bring_clash_royale_to_front():
                    if self._debug:
                        print("⚠ 无法唤出皇室战争页面，继续尝试截图...")
            
            # 2. 等待界面稳定 - 减少等待时间
            time.sleep(0.2)
            
            # 3. 仅在必要时更新weapp_region
            if not skip_bring_to_front:
                self.weapp_region = self._calculate_absolute_weapp_region()
                if self._debug:
                    print(f"更新后的皇室战争区域: {self.weapp_region}")
            
            # 4. 截取WeApp区域（皇室战争区域）
            if self._debug:
                print(f"正在截取皇室战争区域: {self.weapp_region}")
            
            # 5. 保存截图
            filename = os.path.join(self.screenshot_dir, self.get_timestamp_filename(prefix))
            
            # 使用screencapture命令截图，添加-a参数禁用声音，-x参数不显示截图预览
            x, y, width, height = self.weapp_region
            # 构建screencapture命令，-R参数指定区域：x,y,width,height
            screencapture_cmd = ["screencapture", "-a", "-x", "-R", f"{x},{y},{width},{height}", filename]
            subprocess.run(screencapture_cmd, check=True, capture_output=True, text=True)
            
            # 6. 检查截图是否成功生成
            if not os.path.exists(filename):
                raise Exception(f"截图文件未生成: {filename}")
            
            # 7. 快速验证截图尺寸是否符合预期
            try:
                from PIL import Image
                with Image.open(filename) as img:
                    screenshot_size = img.size
                    # 检查截图尺寸是否合理
                    if screenshot_size[0] < 100 or screenshot_size[1] < 100:
                        raise Exception(f"截图尺寸异常: {screenshot_size}")
                    if self._debug:
                        print(f"  截图尺寸: {screenshot_size}")
            except Exception as e:
                if self._debug:
                    print(f"  获取截图尺寸失败: {e}")
            
            if self._debug:
                file_size = os.path.getsize(filename)
                print(f"✅ 成功截取皇室战争界面，保存为: {filename}")
                print(f"  文件大小: {file_size} 字节")
            
            return filename
        except Exception as e:
            if self._debug:
                print(f"✗ 自动截取皇室战争界面失败: {e}")
                import traceback
                traceback.print_exc()
            return None
    
    def screenshot_fullscreen(self, prefix="fullscreen"):
        """截取全屏"""
        try:
            if self._debug:
                print("\n开始截取全屏...")
            
            # 保存截图文件
            filename = os.path.join(self.screenshot_dir, self.get_timestamp_filename(prefix))
            
            # 使用screencapture命令截取全屏，添加-a参数禁用声音，-x参数不显示截图预览
            screencapture_cmd = ["screencapture", "-a", "-x", filename]
            subprocess.run(screencapture_cmd, check=True, capture_output=True, text=True)
            
            # 检查截图是否成功生成
            if not os.path.exists(filename):
                raise Exception(f"截图文件未生成: {filename}")
            
            # 获取截图尺寸
            try:
                from PIL import Image
                with Image.open(filename) as img:
                    screenshot_size = img.size
                    if self._debug:
                        print(f"✓ 成功截取全屏，保存为: {filename}")
                        print(f"  文件大小: {os.path.getsize(filename)} 字节")
                        print(f"  截图尺寸: {screenshot_size}")
            except Exception as e:
                if self._debug:
                    print(f"  获取截图尺寸失败: {e}")
            
            return filename
        except Exception as e:
            if self._debug:
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