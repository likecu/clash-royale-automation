from PIL import Image
import os
from config.config import STATUS_RECOGNITION_CONFIG
from cr.utils import ImageUtils

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
    
    def check_status_button(self, screenshot_gray, status):
        """检查截图中是否存在指定状态的按钮"""
        if status not in self.button_templates or not self.button_templates[status]:
            print(f"  {status}按钮模板未加载，跳过检查")
            return 0.0
        
        # 使用专门的按钮模板匹配算法检查对应状态的按钮
        button_template = self.button_templates[status]
        button_similarity = ImageUtils.button_template_matching(screenshot_gray, button_template)
        print(f"  {status}按钮相似度: {button_similarity:.4f}")
        return button_similarity
    
    def recognize_status(self, screenshot_path):
        """识别当前截图的状态"""
        try:
            # 打开并预处理截图
            screenshot = Image.open(screenshot_path)
            screenshot_gray = ImageUtils.preprocess_image(screenshot)
            
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
                page_similarity = ImageUtils.simple_template_matching(screenshot_gray, template)
                
                # 综合考虑页面相似度和按钮相似度，根据状态调整权重
                button_similarity = button_similarities[status]
                
                # 为不同状态设置不同的权重分配
                if status == "战斗中":
                    # 战斗中状态：提高页面权重，降低按钮权重，减少误判
                    similarity = (page_similarity * 0.8) + (button_similarity * 0.2)
                elif status == "战斗结束":
                    # 战斗结束状态：提高页面权重，降低按钮权重
                    similarity = (page_similarity * 0.9) + (button_similarity * 0.1)
                elif status == "战斗未开始":
                    # 战斗未开始状态：提高页面权重，降低按钮权重
                    similarity = (page_similarity * 0.9) + (button_similarity * 0.1)
                else:
                    # 其他状态：保持原有权重
                    similarity = (page_similarity * 0.4) + (button_similarity * 0.6)
                
                print(f"状态比较: {status} -> 页面相似度: {page_similarity:.4f}, 按钮相似度: {button_similarity:.4f}, 综合相似度: {similarity:.4f}")
                
                # 更新最佳匹配
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_status = status
            
            # 6. 使用配置文件中定义的阈值或默认阈值
            if best_status:
                # 为不同状态设置不同的阈值
                status_thresholds = {
                    "战斗结束": 0.53,  # 降低战斗结束状态的阈值，提高识别率
                    "战斗中": 0.54,   # 降低战斗中状态的阈值，提高识别率
                    "战斗未开始": 0.54,  # 降低战斗未开始状态的阈值，提高识别率
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