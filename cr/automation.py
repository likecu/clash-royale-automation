from cr.screenshot import ScreenshotManager
from cr.status_recognizer import StatusRecognizer
from cr.action_executor import ActionExecutor
from cr.button_marker import ButtonMarker
from cr.yolo_detector import YoloDetector
from PIL import Image, ImageDraw
import os
from config.config import BUTTON_CONFIG

class CRGameAutomation:
    """皇室战争游戏自动化工具，整合截图、状态识别和操作执行功能"""
    
    def __init__(self, use_yolo=True):
        """初始化自动化工具"""
        # 初始化各个模块
        self.screenshot_manager = ScreenshotManager()
        self.status_recognizer = StatusRecognizer()
        self.action_executor = ActionExecutor()
        self.button_marker = ButtonMarker()
        
        # 初始化YOLO检测器
        self.use_yolo = use_yolo
        if use_yolo:
            self.yolo_detector = YoloDetector()
        
        # 按钮位置配置
        self.button_positions = BUTTON_CONFIG
    
    def capture_and_analyze(self, prefix="weapp_auto", execute_action=False, skip_bring_to_front=False):
        """截取屏幕并分析状态，可选择执行相应行为
        
        参数:
            prefix: 截图文件名前缀
            execute_action: 是否执行相应行为，默认不执行
            skip_bring_to_front: 是否跳过窗口前置操作，用于连续截图优化
        """
        print("\n===== 开始捕获并分析屏幕 =====")
        
        # 1. 截取屏幕 - 使用优化后的方法，支持跳过前置操作
        screenshot_path = self.screenshot_manager.auto_screenshot_clash_royale(prefix, skip_bring_to_front=skip_bring_to_front)
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
    
    def detect_battle_elements(self, screenshot_path):
        """检测战斗画面中的元素
        
        参数:
            screenshot_path: 战斗截图路径
            
        返回:
            detected_elements: 检测到的战斗元素
        """
        if not self.use_yolo:
            print("✗ YOLO功能未启用")
            return None
        
        return self.yolo_detector.detect_game_elements(screenshot_path)
    
    def calculate_best_deploy_position(self, screenshot_path):
        """计算最佳下兵位置
        
        参数:
            screenshot_path: 战斗截图路径
            
        返回:
            best_position: 最佳下兵位置 (x, y)
        """
        if not self.use_yolo:
            print("✗ YOLO功能未启用")
            return None
        
        # 检测游戏元素
        detected_elements = self.detect_battle_elements(screenshot_path)
        if not detected_elements:
            return None
        
        # 获取图片形状
        import cv2
        image = cv2.imread(screenshot_path)
        if image is None:
            print(f"✗ 无法加载图片: {screenshot_path}")
            return None
        
        # 计算最佳下兵位置
        best_position = self.yolo_detector.calculate_best_deploy_position(detected_elements, image.shape)
        print(f"✓ 最佳下兵位置计算完成: {best_position}")
        
        return best_position
    
    def analyze_battle_screenshot(self, screenshot_path, output_path=None):
        """分析战斗截图并给出下兵建议
        
        参数:
            screenshot_path: 战斗截图路径
            output_path: 可视化结果输出路径
            
        返回:
            best_position: 最佳下兵位置
        """
        if not self.use_yolo:
            print("✗ YOLO功能未启用")
            return None
        
        print(f"\n===== 开始分析战斗截图: {screenshot_path} =====")
        
        # 检测并可视化结果
        best_position = self.yolo_detector.detect_and_visualize(screenshot_path, output_path)
        
        print("===== 战斗截图分析完成 =====")
        return best_position
    
    def capture_battle_and_analyze(self, prefix="battle_auto"):
        """捕获战斗画面并分析，给出下兵建议
        
        参数:
            prefix: 截图文件名前缀
            
        返回:
            best_position: 最佳下兵位置
        """
        print("\n===== 开始捕获战斗画面 =====")
        
        # 截取屏幕
        screenshot_path = self.screenshot_manager.auto_screenshot_clash_royale(prefix)
        if not screenshot_path:
            print("✗ 截图失败，无法继续分析")
            return None
        
        # 识别状态
        status, similarity = self.status_recognizer.recognize_status(screenshot_path)
        
        if status == "战斗中":
            print(f"✓ 识别为战斗状态，开始分析下兵位置")
            # 分析战斗截图
            best_position = self.analyze_battle_screenshot(screenshot_path)
            return best_position
        else:
            print(f"✗ 当前不是战斗状态: {status}")
            return None