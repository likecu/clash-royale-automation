from PIL import Image
import numpy as np
import subprocess
import time
import os

class ImageUtils:
    """图像处理工具类"""
    
    @staticmethod
    def preprocess_image(img):
        """图片预处理：转换为灰度图并进行简单降噪"""
        # 转换为灰度图
        img_gray = img.convert("L")
        return img_gray
    
    @staticmethod
    def compare_images(img1, img2):
        """比较两张图片的相似度，返回0-1之间的值，1表示完全相同"""
        # 将图片转换为numpy数组
        np1 = np.array(img1)
        np2 = np.array(img2)
        
        # 调整图片尺寸，确保它们大小相同
        if np1.shape != np2.shape:
            # 取较小的尺寸进行比较
            min_h = min(np1.shape[0], np2.shape[0])
            min_w = min(np1.shape[1], np2.shape[1])
            np1 = np1[:min_h, :min_w]
            np2 = np2[:min_h, :min_w]
        
        # 计算像素差异
        diff = np.abs(np1 - np2)
        total_diff = np.sum(diff)
        max_diff = np1.size * 255  # 最大可能差异
        
        # 计算相似度（0-1）
        similarity = 1 - (total_diff / max_diff)
        return similarity
    
    @staticmethod
    def simple_template_matching(screenshot, template):
        """简单高效的模板匹配算法"""
        # 将图片转换为numpy数组
        screenshot_np = np.array(screenshot)
        template_np = np.array(template)
        
        screenshot_h, screenshot_w = screenshot_np.shape
        template_h, template_w = template_np.shape
        
        # 调整模板尺寸与截图完全相同
        template_img = Image.fromarray(template_np)
        resized_template = template_img.resize((screenshot_w, screenshot_h))
        resized_template_np = np.array(resized_template)
        
        # 计算图片差异
        diff = np.abs(screenshot_np - resized_template_np)
        # 计算差异比例
        diff_ratio = np.sum(diff) / (diff.size * 255)
        # 转换为相似度
        similarity = 1 - diff_ratio
        
        return similarity
    
    @staticmethod
    def button_template_matching(screenshot, button_template):
        """专门用于按钮识别的模板匹配算法"""
        # 将图片转换为numpy数组
        screenshot_np = np.array(screenshot)
        button_np = np.array(button_template)
        
        screenshot_h, screenshot_w = screenshot_np.shape
        button_h, button_w = button_np.shape
        
        # 如果按钮尺寸大于截图尺寸，调整按钮尺寸
        if button_h > screenshot_h or button_w > screenshot_w:
            return 0.0
        
        best_similarity = 0.0
        
        # 在截图中滑动按钮模板，寻找最佳匹配
        # 只在可能出现按钮的区域搜索，减少计算量
        search_region_h = screenshot_h - button_h + 1
        search_region_w = screenshot_w - button_w + 1
        
        # 只搜索屏幕下半部分，因为对战按钮通常在底部
        start_y = int(search_region_h * 0.5)
        end_y = search_region_h
        
        for y in range(start_y, end_y, 5):  # 步长为5，减少计算量
            for x in range(0, search_region_w, 5):  # 步长为5，减少计算量
                # 截取当前窗口
                window = screenshot_np[y:y+button_h, x:x+button_w]
                
                # 计算差异
                diff = np.abs(window - button_np)
                diff_ratio = np.sum(diff) / (diff.size * 255)
                similarity = 1 - diff_ratio
                
                # 更新最佳相似度
                if similarity > best_similarity:
                    best_similarity = similarity
        
        return best_similarity
    
    @staticmethod
    def find_button_position(interface_img, button_img):
        """使用模板匹配找到按钮在界面中的位置"""
        # 将图片转换为numpy数组
        interface_np = np.array(interface_img)
        button_np = np.array(button_img)
        
        # 获取界面和按钮的尺寸
        if len(interface_np.shape) == 3:
            interface_h, interface_w, _ = interface_np.shape
        else:
            interface_h, interface_w = interface_np.shape
        
        if len(button_np.shape) == 3:
            button_h, button_w, _ = button_np.shape
        else:
            button_h, button_w = button_np.shape
        
        # 计算需要遍历的区域
        h_search = interface_h - button_h
        w_search = interface_w - button_w
        
        best_match = (0, 0)
        min_diff = float('inf')
        
        # 遍历界面，寻找与按钮最匹配的区域
        for y in range(0, h_search, 5):  # 步长为5，加快搜索速度
            for x in range(0, w_search, 5):
                # 截取当前区域
                if len(interface_np.shape) == 3:
                    region = interface_np[y:y+button_h, x:x+button_w, :]
                    # 计算与按钮的差异
                    diff = np.sum(np.abs(region - button_np))
                else:
                    region = interface_np[y:y+button_h, x:x+button_w]
                    # 计算与按钮的差异
                    diff = np.sum(np.abs(region - button_np))
                # 更新最佳匹配
                if diff < min_diff:
                    min_diff = diff
                    best_match = (x, y)
        
        return best_match

class SystemUtils:
    """系统工具类"""
    
    @staticmethod
    def run_osascript(script):
        """运行AppleScript脚本"""
        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
        return result
    
    @staticmethod
    def get_timestamp_filename(prefix="auto"):
        """生成带时间戳的文件名"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{timestamp}.png"
    
    @staticmethod
    def ensure_dir_exists(dir_path):
        """确保目录存在"""
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
    
    @staticmethod
    def bring_window_to_front(app_name):
        """将指定应用的窗口置顶"""
        try:
            # 使用AppleScript将应用置顶
            applescript = f'''tell application "System Events"
    # 确保进程存在
    if exists process "{app_name}" then
        # 强制将应用置顶
        tell process "{app_name}"
            set frontmost to true
            delay 0.5
            # 确保至少有一个窗口
            if not (exists window 1) then
                # 尝试打开应用窗口
                try
                    click menu item 1 of menu 1 of menu bar item "文件" of menu bar 1
                    delay 1
                end try
            end if
        end tell
        return true
    else
        return false
    end if
end tell'''
            
            result = SystemUtils.run_osascript(applescript)
            return "true" in result.stdout
        except Exception as e:
            print(f"将应用{app_name}置顶失败: {e}")
            return False

class WeChatUtils:
    """微信相关工具类"""
    
    @staticmethod
    def bring_wechat_to_front():
        """将微信窗口置顶"""
        return SystemUtils.bring_window_to_front("WeChat")
    
    @staticmethod
    def get_wechat_window_position():
        """获取微信窗口的位置和大小"""
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
            
            return {
                "x": wx_x,
                "y": wx_y,
                "width": wx_width,
                "height": wx_height
            }
        except Exception as e:
            print(f"获取微信窗口位置失败: {e}")
            # 返回默认值
            return {
                "x": 400,
                "y": 100,
                "width": 800,
                "height": 600
            }