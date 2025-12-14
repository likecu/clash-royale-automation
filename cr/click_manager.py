import subprocess
import time
import os
from config.config import SCREENSHOT_CONFIG
from cr.utils import WeChatUtils

class ClickManager:
    """点击管理器，封装点击操作并进行边界检查"""
    
    def __init__(self):
        self.config = SCREENSHOT_CONFIG
        self.wechat_process_name = self.config["wechat_process_name"]
        # 皇室战争窗口区域配置 - 延迟初始化，需要时才计算
        self.cr_window_region = None
        # 移除初始化时的打印信息
    
    def _get_cr_window_region(self):
        """获取皇室战争的窗口区域，格式为(x, y, width, height)"""
        try:
            # 激活微信窗口
            WeChatUtils.bring_wechat_to_front()
            time.sleep(0.1)
            
            # 获取微信窗口位置和大小
            wx_window = WeChatUtils.get_wechat_window_position()
            wx_x = wx_window["x"]
            wx_y = wx_window["y"]
            
            # 从配置文件获取皇室战争小程序在微信窗口内的相对区域
            weapp_relative_region = self.config["weapp_relative_region"]
            rel_x, rel_y, rel_width, rel_height = weapp_relative_region
            
            # 动态计算皇室战争小程序的绝对区域
            # 微信窗口左上角为基准点，加上小程序在微信窗口内的相对位置
            abs_x = wx_x + rel_x
            abs_y = wx_y + rel_y
            width = rel_width
            height = rel_height
            
            return (abs_x, abs_y, width, height)
        except Exception as e:
            print(f"获取微信窗口信息失败: {e}")
            # 如果获取失败，使用默认值
            wx_x, wx_y = (400, 100)  # 默认窗口位置
            weapp_relative_region = self.config["weapp_relative_region"]
            rel_x, rel_y, rel_width, rel_height = weapp_relative_region
            # 使用默认窗口位置和配置的相对区域
            return (wx_x + rel_x, wx_y + rel_y, rel_width, rel_height)
    
    def update_cr_window_region(self):
        """更新皇室战争窗口区域"""
        self.cr_window_region = self._get_cr_window_region()
        print(f"已更新皇室战争窗口区域: {self.cr_window_region}")
    
    def get_cr_window_position(self):
        """获取皇室战争窗口的位置和大小"""
        # 确保窗口区域已初始化
        if self.cr_window_region is None:
            self.cr_window_region = self._get_cr_window_region()
        x, y, width, height = self.cr_window_region
        return {
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "right": x + width,
            "bottom": y + height
        }
    
    def is_position_in_cr_window(self, x, y):
        """判断指定坐标是否在皇室战争窗口内"""
        cr_pos = self.get_cr_window_position()
        return cr_pos["x"] <= x <= cr_pos["right"] and cr_pos["y"] <= y <= cr_pos["bottom"]
    
    def is_position_on_screen(self, x, y):
        """判断指定坐标是否在屏幕范围内"""
        # 使用系统命令获取屏幕大小
        try:
            # 使用 AppleScript 获取屏幕大小
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
        return 0 <= x < screen_width and 0 <= y < screen_height
    
    def check_click_position(self, x, y):
        """检查点击位置是否合法
        
        Args:
            x: 点击的x坐标
            y: 点击的y坐标
            
        Returns:
            bool: 是否可以点击
            str: 错误信息（如果不可点击）
        """
        # 1. 检查是否在屏幕范围内
        if not self.is_position_on_screen(x, y):
            # 重新获取屏幕大小用于错误信息
            try:
                applescript = '''tell application "Finder"
    set screen_resolution to bounds of window of desktop
    return screen_resolution
end tell'''
                result = subprocess.run(["osascript", "-e", applescript], check=True, capture_output=True, text=True)
                bounds = result.stdout.strip().replace("{", "").replace("}", "").split(", ")
                screen_width = int(bounds[2])
                screen_height = int(bounds[3])
            except Exception as e:
                screen_width, screen_height = 1920, 1080
            return False, f"点击位置({x}, {y})超出屏幕边界({screen_width}, {screen_height})"
        
        # 2. 检查是否在皇室战争窗口内
        if not self.is_position_in_cr_window(x, y):
            cr_pos = self.get_cr_window_position()
            return False, f"点击位置({x}, {y})超出皇室战争窗口范围({cr_pos['x']}, {cr_pos['y']}, {cr_pos['width']}, {cr_pos['height']})"
        
        return True, ""
    
    def _convert_percentage_to_absolute(self, x, y):
        """将百分比坐标转换为绝对坐标
        
        Args:
            x: 百分比x坐标 (0-100) 或绝对x坐标
            y: 百分比y坐标 (0-100) 或绝对y坐标
            
        Returns:
            tuple: (绝对x坐标, 绝对y坐标)
        """
        # 判断是否为百分比坐标（如果x或y在0-100范围内）
        if 0 <= x <= 100 and 0 <= y <= 100:
            print(f"  检测到百分比坐标: ({x}%, {y}%)")
            # 确保皇室战争窗口区域已初始化
            if self.cr_window_region is None:
                self.cr_window_region = self._get_cr_window_region()
            # 获取皇室战争窗口区域
            cr_x, cr_y, cr_width, cr_height = self.cr_window_region
            # 转换为绝对坐标
            abs_x = cr_x + (x / 100) * cr_width
            abs_y = cr_y + (y / 100) * cr_height
            return (int(abs_x), int(abs_y))
        else:
            # 已经是绝对坐标
            return (x, y)
    
    def click(self, x, y):
        """执行点击操作
        
        Args:
            x: 点击的x坐标（可以是绝对坐标或百分比坐标）
            y: 点击的y坐标（可以是绝对坐标或百分比坐标）
            
        Returns:
            bool: 是否点击成功
        """
        print(f"\n=== 执行点击操作 ===")
        print(f"请求点击位置: ({x}, {y})")
        
        # 将百分比坐标转换为绝对坐标
        abs_x, abs_y = self._convert_percentage_to_absolute(x, y)
        if (abs_x, abs_y) != (x, y):
            print(f"  转换为绝对坐标: ({abs_x}, {abs_y})")
        
        # 检查点击位置
        is_valid, error_msg = self.check_click_position(abs_x, abs_y)
        if not is_valid:
            print(f"✗ 点击失败: {error_msg}")
            return False
        
        try:
            # 激活微信窗口
            applescript = '''tell application "WeChat"
    activate
    delay 0.1
end tell'''
            subprocess.run(["osascript", "-e", applescript], check=True, capture_output=True, text=True)
            time.sleep(0.1)
            
            # 只使用cliclick执行点击，不需要先移动鼠标
            print(f"  使用cliclick点击位置: ({abs_x}, {abs_y})")
            # 直接执行点击，cliclick的c:命令会自动定位到指定位置
            subprocess.run(["cliclick", f"c:{abs_x},{abs_y}"], check=True, capture_output=True, text=True)
            
            print(f"✓ 点击成功: ({abs_x}, {abs_y})")
            return True
        except Exception as e:
            print(f"✗ 点击执行失败: {e}")
            return False
    
    def click_with_retry(self, x, y, retry_count=3, interval=1.0):
        """带重试机制的点击操作
        
        Args:
            x: 点击的x坐标（可以是绝对坐标或百分比坐标）
            y: 点击的y坐标（可以是绝对坐标或百分比坐标）
            retry_count: 重试次数
            interval: 重试间隔（秒）
            
        Returns:
            bool: 是否点击成功
        """
        for i in range(retry_count):
            if self.click(x, y):
                return True
            if i < retry_count - 1:
                print(f"  等待{interval}秒后重试...")
                time.sleep(interval)
        return False
    
    def double_click(self, x, y):
        """执行双击操作
        
        Args:
            x: 点击的x坐标（可以是绝对坐标或百分比坐标）
            y: 点击的y坐标（可以是绝对坐标或百分比坐标）
            
        Returns:
            bool: 是否点击成功
        """
        print(f"\n=== 执行双击操作 ===")
        print(f"请求双击位置: ({x}, {y})")
        
        # 将百分比坐标转换为绝对坐标
        abs_x, abs_y = self._convert_percentage_to_absolute(x, y)
        if (abs_x, abs_y) != (x, y):
            print(f"  转换为绝对坐标: ({abs_x}, {abs_y})")
        
        # 检查点击位置
        is_valid, error_msg = self.check_click_position(abs_x, abs_y)
        if not is_valid:
            print(f"✗ 双击失败: {error_msg}")
            return False
        
        try:
            # 激活微信窗口
            applescript = '''tell application "WeChat"
    activate
    delay 0.1
end tell'''
            subprocess.run(["osascript", "-e", applescript], check=True, capture_output=True, text=True)
            time.sleep(0.1)
            
            # 只使用cliclick执行双击
            print(f"  使用cliclick双击位置: ({abs_x}, {abs_y})")
            subprocess.run(["cliclick", f"dc:{abs_x},{abs_y}"], check=True, capture_output=True, text=True)
            
            print(f"✓ 双击成功: ({abs_x}, {abs_y})")
            return True
        except Exception as e:
            print(f"✗ 双击执行失败: {e}")
            return False
    
    def move_mouse(self, x, y, duration=0.2):
        """移动鼠标到指定位置
        
        Args:
            x: 目标x坐标（可以是绝对坐标或百分比坐标）
            y: 目标y坐标（可以是绝对坐标或百分比坐标）
            duration: 移动持续时间（秒）
            
        Returns:
            bool: 是否移动成功
        """
        print(f"\n=== 执行鼠标移动操作 ===")
        print(f"请求移动到位置: ({x}, {y})")
        
        # 将百分比坐标转换为绝对坐标
        abs_x, abs_y = self._convert_percentage_to_absolute(x, y)
        if (abs_x, abs_y) != (x, y):
            print(f"  转换为绝对坐标: ({abs_x}, {abs_y})")
        
        # 检查目标位置
        is_valid, error_msg = self.check_click_position(abs_x, abs_y)
        if not is_valid:
            print(f"✗ 鼠标移动失败: {error_msg}")
            return False
        
        try:
            # 激活微信窗口
            applescript = '''tell application "WeChat"
    activate
    delay 0.1
end tell'''
            subprocess.run(["osascript", "-e", applescript], check=True, capture_output=True, text=True)
            time.sleep(0.1)
            
            # 使用cliclick移动鼠标，-e参数指定持续时间（毫秒）
            print(f"  移动鼠标到: ({abs_x}, {abs_y})")
            duration_ms = int(duration * 1000)  # 转换为毫秒
            subprocess.run(["cliclick", f"-e", str(duration_ms), f"m:{abs_x},{abs_y}"], check=True, capture_output=True, text=True)
            
            print(f"✓ 鼠标移动成功: ({abs_x}, {abs_y})")
            return True
        except Exception as e:
            print(f"✗ 鼠标移动执行失败: {e}")
            return False

# 测试代码（如果直接运行此文件）
if __name__ == "__main__":
    click_manager = ClickManager()
    
    # 测试获取窗口位置
    print("皇室战争窗口位置:", click_manager.get_cr_window_position())
    
    # 测试位置检查
    test_positions = [
        (450, 200),  # 在窗口内
        (400, 200),  # 在窗口外（左侧）
        (900, 200),  # 在窗口外（右侧）
        (450, 100),  # 在窗口外（上方）
        (450, 700),  # 在窗口外（下方）
        (1920, 1080)  # 超出屏幕范围
    ]
    
    for x, y in test_positions:
        is_valid, error_msg = click_manager.check_click_position(x, y)
        status = "✓ 合法" if is_valid else f"✗ 非法: {error_msg}"
        print(f"位置 ({x}, {y}): {status}")
    
    # 测试点击操作（注释掉以避免实际点击）
    # click_manager.click(450, 200, use_cliclick=False)