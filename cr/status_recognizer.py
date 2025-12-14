from PIL import Image
import numpy as np
import os
from config.config import STATUS_RECOGNITION_CONFIG

class StatusRecognizer:
    """屏幕状态识别器，用于判断当前截图属于什么状态"""
    
    def __init__(self):
        self.config = STATUS_RECOGNITION_CONFIG
        self.status_templates = self.config["status_templates"]
        # 按钮模板映射：状态 -> 按钮模板
        self.button_templates = {}
        # 加载所有状态模板
        self.load_templates()
        # 加载所有状态对应的按钮模板
        self.load_all_button_templates()
    
    def load_templates(self):
        """加载所有状态模板图片"""
        print("加载状态模板...")
        for status, config in self.status_templates.items():
            try:
                template_img = Image.open(config["template_path"])
                # 转换为灰度图，减少颜色干扰，提高识别率
                template_img = template_img.convert("L")
                self.status_templates[status]["template_img"] = template_img
                # 保存模板原始尺寸
                self.status_templates[status]["template_size"] = template_img.size
                print(f"✓ 成功加载模板: {status} -> {config['template_path']}")
                print(f"  模板尺寸: {template_img.size}")
            except Exception as e:
                print(f"✗ 加载模板失败: {status} -> {config['template_path']}")
                print(f"  错误信息: {e}")
    
    def load_all_button_templates(self):
        """加载所有状态对应的按钮模板"""
        print("加载所有按钮模板...")
        
        # 状态到按钮模板路径的映射
        status_to_button_path = {
            "战斗未开始": "png/战斗未开始/对战按钮.png",
            "战斗中": "png/战斗中/表情按钮.png",
            "战斗结束": "png/战斗结束/战斗结束确认按钮.png",
            "开宝箱": "png/开宝箱/开宝箱界面按钮.png"
        }
        
        for status, button_path in status_to_button_path.items():
            try:
                button_template = Image.open(button_path)
                button_template = button_template.convert("L")
                self.button_templates[status] = button_template
                print(f"✓ 成功加载按钮模板: {status} -> {button_path}")
                print(f"  按钮模板尺寸: {button_template.size}")
            except Exception as e:
                print(f"✗ 加载按钮模板失败: {status} -> {button_path}")
                print(f"  错误信息: {e}")
                self.button_templates[status] = None
    
    def preprocess_image(self, img):
        """图片预处理：转换为灰度图并进行简单降噪"""
        # 转换为灰度图
        img_gray = img.convert("L")
        return img_gray
    
    def simple_template_matching(self, screenshot, template):
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
    
    def button_template_matching(self, screenshot, button_template):
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
    
    def check_status_button(self, screenshot_gray, status):
        """检查截图中是否存在指定状态的按钮"""
        if status not in self.button_templates or not self.button_templates[status]:
            print(f"  {status}按钮模板未加载，跳过检查")
            return 0.0
        
        # 使用专门的按钮模板匹配算法检查对应状态的按钮
        button_template = self.button_templates[status]
        button_similarity = self.button_template_matching(screenshot_gray, button_template)
        print(f"  {status}按钮相似度: {button_similarity:.4f}")
        return button_similarity
    
    def compare_images(self, img1, img2):
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
    
    def recognize_status(self, screenshot_path):
        """识别当前截图的状态"""
        try:
            # 打开并预处理截图
            screenshot = Image.open(screenshot_path)
            screenshot_gray = self.preprocess_image(screenshot)
            
            best_status = None
            best_similarity = 0
            
            # 1. 首先检查所有状态的按钮，记录按钮相似度
            print("\n=== 开始按钮优先检测 ===")
            
            button_similarities = {}
            
            for status in self.button_templates:
                button_similarity = self.check_status_button(screenshot_gray, status)
                button_similarities[status] = button_similarity
            
            # 找出按钮相似度最高的状态
            max_button_similarity = 0
            best_button_status = None
            
            for status, button_similarity in button_similarities.items():
                if button_similarity > max_button_similarity:
                    max_button_similarity = button_similarity
                    best_button_status = status
            
            # 只有当最高按钮相似度明显高于其他状态时，才直接返回该状态
            is_significant = True
            for status, button_similarity in button_similarities.items():
                if status != best_button_status and abs(max_button_similarity - button_similarity) < 0.05:
                    is_significant = False
                    break
            
            # 如果最高按钮相似度超过阈值且明显高于其他状态，直接返回该状态
            if max_button_similarity >= 0.85 and is_significant:
                print(f"\n✓ 按钮相似度最高且明显高于其他状态，直接返回: {best_button_status} (按钮相似度: {max_button_similarity:.4f})")
                return best_button_status, max_button_similarity
            
            # 5. 进行完整的状态识别，结合页面相似度和按钮相似度
            print("\n=== 进行完整状态识别 ===")
            
            for status, config in self.status_templates.items():
                if "template_img" not in config:
                    continue
                
                template = config["template_img"]
                
                # 使用简单模板匹配算法获取页面相似度
                page_similarity = self.simple_template_matching(screenshot_gray, template)
                
                # 综合考虑页面相似度和按钮相似度，按钮权重更高
                button_similarity = button_similarities[status]
                # 页面权重0.5，按钮权重0.5
                similarity = (page_similarity * 0.5) + (button_similarity * 0.5)
                
                print(f"状态比较: {status} -> 页面相似度: {page_similarity:.4f}, 按钮相似度: {button_similarity:.4f}, 综合相似度: {similarity:.4f}")
                
                # 更新最佳匹配
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_status = status
            
            # 6. 使用配置文件中定义的阈值或默认阈值
            if best_status:
                # 为不同状态设置不同的阈值
                status_thresholds = {
                    "战斗结束": 0.60,  # 降低战斗结束状态的阈值
                    "战斗中": 0.65,
                    "战斗未开始": 0.65,
                    "开宝箱": 0.65
                }
                
                threshold = status_thresholds[best_status]
                print(f"使用状态 '{best_status}' 的阈值: {threshold}")
                
                if best_similarity >= threshold:
                    return best_status, best_similarity
                else:
                    return None, best_similarity
            else:
                # 如果没有找到最佳状态，返回None
                return None, 0
        
        except Exception as e:
            print(f"识别状态失败: {e}")
            import traceback
            traceback.print_exc()
            return None, 0
    
    def process_screenshot(self, screenshot_path):
        """处理截图：识别状态"""
        print(f"\n处理截图: {screenshot_path}")
        print("=" * 50)
        
        # 识别状态
        status, similarity = self.recognize_status(screenshot_path)
        
        if status:
            print(f"✓ 识别结果: {status} (相似度: {similarity:.4f})")
        else:
            print(f"✗ 无法识别状态 (最高相似度: {similarity:.4f})")
        
        print("=" * 50)
        return status, similarity