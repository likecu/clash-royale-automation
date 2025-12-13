from PIL import Image
import numpy as np
import os
from config.config import STATUS_RECOGNITION_CONFIG

class StatusRecognizer:
    """屏幕状态识别器，用于判断当前截图属于什么状态"""
    
    def __init__(self):
        self.config = STATUS_RECOGNITION_CONFIG
        self.status_templates = self.config["status_templates"]
        # 加载所有状态模板
        self.load_templates()
    
    def load_templates(self):
        """加载所有状态模板图片"""
        print("加载状态模板...")
        for status, config in self.status_templates.items():
            try:
                template_img = Image.open(config["template_path"])
                # 转换为RGB模式，确保一致性
                template_img = template_img.convert("RGB")
                self.status_templates[status]["template_img"] = template_img
                print(f"✓ 成功加载模板: {status} -> {config['template_path']}")
            except Exception as e:
                print(f"✗ 加载模板失败: {status} -> {config['template_path']}")
                print(f"  错误信息: {e}")
    
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
            np1 = np1[:min_h, :min_w, :]
            np2 = np2[:min_h, :min_w, :]
        
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
            screenshot = screenshot.convert("RGB")
            
            best_status = None
            best_similarity = 0
            
            # 与所有状态模板进行比较
            for status, config in self.status_templates.items():
                if "template_img" not in config:
                    continue
                
                template = config["template_img"]
                similarity = self.compare_images(screenshot, template)
                
                print(f"状态比较: {status} -> 相似度: {similarity:.4f}")
                
                # 更新最佳匹配
                if similarity > best_similarity and similarity >= config["threshold"]:
                    best_similarity = similarity
                    best_status = status
            
            return best_status, best_similarity
        
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