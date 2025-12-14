from cr.screenshot import ScreenshotManager
from cr.status_recognizer import StatusRecognizer
from cr.action_executor import ActionExecutor
from cr.button_marker import ButtonMarker
from PIL import Image, ImageDraw
import os
from config.config import BUTTON_CONFIG

class CRGameAutomation:
    """皇室战争游戏自动化工具，整合截图、状态识别和操作执行功能"""
    
    def __init__(self):
        # 初始化各个模块
        self.screenshot_manager = ScreenshotManager()
        self.status_recognizer = StatusRecognizer()
        self.action_executor = ActionExecutor()
        self.button_marker = ButtonMarker()
        # 按钮位置配置
        self.button_positions = BUTTON_CONFIG
    
    def capture_and_analyze(self, prefix="weapp_auto", execute_action=False):
        """截取屏幕并分析状态，可选择执行相应行为
        
        参数:
            prefix: 截图文件名前缀
            execute_action: 是否执行相应行为，默认不执行
        """
        print("\n===== 开始捕获并分析屏幕 =====")
        
        # 1. 截取屏幕
        screenshot_path = self.screenshot_manager.auto_screenshot_weapp(prefix)
        if not screenshot_path:
            print("✗ 截图失败，无法继续分析")
            return None, None
        
        # 2. 分析状态
        status, similarity = self.status_recognizer.recognize_status(screenshot_path)
        
        if status:
            print(f"✓ 成功识别状态: {status} (相似度: {similarity:.4f})")
            # 3. 执行相应行为（如果execute_action为True）
            if execute_action:
                self.execute_smart_action(status, screenshot_path)
        else:
            print(f"✗ 无法识别状态 (最高相似度: {similarity:.4f})")
        
        print("===== 捕获分析完成 =====")
        return status, screenshot_path
    
    def execute_smart_action(self, status, screenshot_path):
        """根据状态执行智能行为"""
        print(f"\n执行智能行为: {status}")
        return self.action_executor.execute_action(status)
    
    def analyze_existing_screenshot(self, screenshot_path):
        """分析已存在的截图"""
        if not os.path.exists(screenshot_path):
            print(f"✗ 截图文件不存在: {screenshot_path}")
            return None
        
        return self.status_recognizer.process_screenshot(screenshot_path)
    
    def batch_analyze_screenshots(self, screenshot_dir="png"):
        """批量分析指定目录下的截图"""
        print(f"\n===== 开始批量分析截图 =====")
        print(f"分析目录: {screenshot_dir}")
        
        # 遍历目录下的所有PNG文件
        results = []
        for root, dirs, files in os.walk(screenshot_dir):
            for file in files:
                if file.endswith(".png"):
                    file_path = os.path.join(root, file)
                    status, similarity = self.status_recognizer.recognize_status(file_path)
                    results.append((file_path, status, similarity))
        
        # 输出结果
        print("\n批量分析结果:")
        print("-" * 70)
        print(f"{'文件路径':<50} {'状态':<15} {'相似度':<10}")
        print("-" * 70)
        
        for file_path, status, similarity in results:
            status_str = status if status else "未知"
            # 分开格式化，避免复合格式问题
            file_name = os.path.basename(file_path).ljust(50)
            status_str = status_str.ljust(15)
            similarity_str = f"{similarity:.4f}".ljust(10)
            print(f"{file_name} {status_str} {similarity_str}")
        
        print("-" * 70)
        print(f"总计分析: {len(results)} 个文件")
        print("===== 批量分析完成 =====")
        
        return results
    
    def mark_button_on_screenshot(self, screenshot_path, status):
        """在截图上标记按钮位置"""
        if not os.path.exists(screenshot_path):
            print(f"✗ 截图文件不存在: {screenshot_path}")
            return None
        
        if status not in self.button_positions:
            print(f"✗ 未知状态: {status}")
            return None
        
        try:
            # 打开截图
            img = Image.open(screenshot_path)
            draw = ImageDraw.Draw(img)
            
            # 标记所有按钮
            for button_name, pos in self.button_positions[status].items():
                # 绘制红色边框
                rect_size = 40  # 边框大小
                x, y = pos
                draw.rectangle([
                    (x - rect_size/2, y - rect_size/2),
                    (x + rect_size/2, y + rect_size/2)
                ], outline=(255, 0, 0), width=3)
                
                # 绘制按钮名称
                draw.text((x - rect_size/2, y - rect_size/2 - 20), button_name, fill=(255, 0, 0))
            
            # 保存标记后的截图
            marked_path = screenshot_path.replace(".png", "_标记.png")
            img.save(marked_path)
            print(f"✓ 已标记按钮，保存为: {marked_path}")
            
            return marked_path
        
        except Exception as e:
            print(f"✗ 标记按钮失败: {e}")
            return None
    
    def mark_all_buttons(self):
        """标记所有场景的按钮位置"""
        return self.button_marker.mark_all_buttons()
    
    def verify_marked_buttons(self, marked_files):
        """验证标记的按钮位置"""
        return self.button_marker.verify_all_marked_files(marked_files)