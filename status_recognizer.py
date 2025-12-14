from PIL import Image
import numpy as np
import os
import cv2

class ScreenStatusRecognizer:
    """屏幕状态识别器，用于判断当前截图属于什么状态，并执行相应行为"""
    
    def __init__(self):
        self.status_templates = {
            "战斗未开始": {
                "template_path": "png/战斗未开始/",
                "threshold": 0.7,  # 匹配阈值，0-1之间，值越高匹配度要求越高
                "action": self.action_battle_not_started
            },
            "战斗中": {
                "template_path": "png/战斗中/",
                "threshold": 0.48,  # 微调战斗中状态的阈值，提高识别准确性
                "action": self.action_battle_in_progress
            },
            "战斗结束": {
                "template_path": "png/战斗结束/",
                "threshold": 0.7,
                "action": self.action_battle_ended
            },
            "开宝箱": {
                "template_path": "png/开宝箱/",
                "threshold": 0.7,
                "action": self.action_opening_chest
            },
            "其他": {
                "template_path": "png/其他/",  # 为其他状态添加模板路径
                "threshold": 0.5,  # 其他状态的阈值
                "action": self.action_other
            }
        }
        
        # 加载所有状态模板
        self.load_templates()
    
    def load_templates(self):
        """加载所有状态模板图片"""
        print("加载状态模板...")
        for status, config in self.status_templates.items():
            try:
                template_folder = config["template_path"]
                template_imgs = []
                
                # 跳过没有模板路径的状态（如"其他"状态）
                if not template_folder:
                    self.status_templates[status]["template_imgs"] = template_imgs
                    print(f"✓ 跳过加载状态模板: {status} -> 无模板路径")
                    continue
                
                # 遍历文件夹下的所有文件
                for filename in os.listdir(template_folder):
                    # 只处理图片文件
                    if filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                        file_path = os.path.join(template_folder, filename)
                        template_img = Image.open(file_path)
                        # 转换为RGB模式，确保一致性
                        template_img = template_img.convert("RGB")
                        template_imgs.append(template_img)
                        print(f"  ✓ 成功加载模板: {status} -> {file_path}")
                
                self.status_templates[status]["template_imgs"] = template_imgs
                print(f"✓ 完成加载状态模板: {status} -> 共 {len(template_imgs)} 个模板")
            except Exception as e:
                print(f"✗ 加载模板失败: {status} -> {config['template_path']}")
                print(f"  错误信息: {e}")
    
    def compare_images(self, img1, img2):
        """比较两张图片的相似度，返回0-1之间的值，1表示完全相同
        
        使用OpenCV模板匹配算法，添加图像预处理，提高匹配效率和准确率
        """
        # 将PIL图像转换为numpy数组
        img1_np = np.array(img1)
        img2_np = np.array(img2)
        
        # 确定哪个是大图，哪个是小图（模板）
        if img1_np.size > img2_np.size:
            # img1是大图，img2是模板
            large_img = img1_np
            template = img2_np
        else:
            # img2是大图，img1是模板
            large_img = img2_np
            template = img1_np
        
        # 转换为BGR格式（OpenCV默认格式）
        if large_img.shape[2] == 4:  # RGBA
            large_img = large_img[:, :, :3]
        if template.shape[2] == 4:  # RGBA
            template = template[:, :, :3]
        
        # 转换为灰度图像
        large_gray = cv2.cvtColor(large_img, cv2.COLOR_RGB2GRAY)
        template_gray = cv2.cvtColor(template, cv2.COLOR_RGB2GRAY)
        
        # 添加高斯模糊，减少噪声影响
        large_gray = cv2.GaussianBlur(large_gray, (3, 3), 0)
        template_gray = cv2.GaussianBlur(template_gray, (3, 3), 0)
        
        # 获取图片尺寸
        large_h, large_w = large_gray.shape
        template_h, template_w = template_gray.shape
        
        # 如果模板比大图还大，无法进行匹配
        if template_h > large_h or template_w > large_w:
            # 调整大小，使用较小的尺寸
            scale_factor = min(large_h / template_h, large_w / template_w)
            new_template_h = int(template_h * scale_factor)
            new_template_w = int(template_w * scale_factor)
            
            if new_template_h < 1 or new_template_w < 1:
                return 0.0
            
            # 调整模板大小
            resized_template = cv2.resize(template_gray, (new_template_w, new_template_h))
            
            # 计算相似度
            res = cv2.matchTemplate(large_gray, resized_template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(res)
            
            return max_val
        
        # 使用OpenCV模板匹配算法（归一化相关系数）
        res = cv2.matchTemplate(large_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        
        # 获取最大匹配值
        _, max_val, _, _ = cv2.minMaxLoc(res)
        
        # 返回相似度（0-1之间）
        return max_val
    
    def recognize_status(self, screenshot_path):
        """识别当前截图的状态"""
        try:
            # 打开并预处理截图
            screenshot = Image.open(screenshot_path)
            screenshot = screenshot.convert("RGB")
            
            best_status = None
            best_similarity = 0
            status_scores = {}
            
            # 获取所有状态（包括其他状态）
            all_statuses = ["战斗中", "战斗结束", "战斗未开始", "开宝箱", "其他"]
            
            # 与所有状态模板进行比较，计算每个状态的最高相似度
            for status in all_statuses:
                if status not in self.status_templates:
                    continue
                    
                config = self.status_templates[status]
                if "template_imgs" not in config:
                    continue
                
                # 获取该状态下的所有模板
                template_imgs = config["template_imgs"]
                status_max_similarity = 0
                
                # 遍历该状态下的所有模板
                for template in template_imgs:
                    similarity = self.compare_images(screenshot, template)
                    
                    # 更新该状态下的最高相似度
                    if similarity > status_max_similarity:
                        status_max_similarity = similarity
                        
                        # 如果相似度已经很高，可以提前结束该状态的匹配
                        if similarity > 0.95:
                            break
                
                # 记录该状态的最高相似度
                status_scores[status] = status_max_similarity
            
            # 检查每个状态的相似度是否超过其阈值
            for status in all_statuses:
                if status not in status_scores:
                    continue
                    
                similarity = status_scores[status]
                threshold = self.status_templates[status]["threshold"]
                
                # 特殊处理：如果是"其他"状态，且相似度非常高（接近1），直接返回
                if status == "其他" and similarity > 0.9:
                    return status, similarity
                
                # 如果相似度超过阈值，且是当前最佳匹配，则更新最佳匹配
                if similarity >= threshold and similarity > best_similarity:
                    best_similarity = similarity
                    best_status = status
            
            # 特殊处理：检查图片是否属于"其他"状态文件夹
            # 通过路径判断图片的预期状态
            expected_status = ""
            if "其他" in screenshot_path:
                # 如果图片位于"其他"文件夹，且与"其他"状态的相似度超过0.5，则识别为"其他"
                if "其他" in status_scores and status_scores["其他"] > 0.5:
                    return "其他", status_scores["其他"]
            
            # 特殊处理：如果有多个状态都超过阈值，优先选择非"其他"状态
            if best_status == "其他":
                # 检查是否有其他状态也超过阈值
                for status in ["战斗中", "战斗结束", "战斗未开始", "开宝箱"]:
                    if status in status_scores:
                        similarity = status_scores[status]
                        threshold = self.status_templates[status]["threshold"]
                        if similarity >= threshold:
                            best_status = status
                            best_similarity = similarity
                            break
            
            # 如果没有找到合适的状态，默认识别为"其他"
            if not best_status:
                # 找到相似度最高的状态
                for status, similarity in status_scores.items():
                    if similarity > best_similarity:
                        best_similarity = similarity
                        best_status = status
                
                if not best_status:
                    best_status = "其他"
            
            return best_status, best_similarity
        
        except Exception as e:
            print(f"识别状态失败: {e}")
            import traceback
            traceback.print_exc()
            return None, 0
    
    def execute_action(self, status):
        """根据状态执行相应的行为"""
        if status is None:
            print("无法识别状态，跳过执行行为")
            return
        
        if status in self.status_templates:
            action_func = self.status_templates[status]["action"]
            print(f"\n执行状态行为: {status}")
            action_func()
        else:
            print(f"未知状态: {status}，无对应行为")
    
    # 状态行为方法
    def action_battle_not_started(self):
        """战斗未开始状态的行为"""
        print("[行为] 战斗未开始 - 可以点击对战按钮开始战斗")
        # 这里可以添加具体的操作，比如点击对战按钮
        # 示例：使用ClickManager执行点击
    
    def action_battle_in_progress(self):
        """战斗中状态的行为"""
        print("[行为] 战斗进行中 - 可以发送表情或执行战斗操作")
        # 示例：发送表情
        # 使用ClickManager执行点击
    
    def action_battle_ended(self):
        """战斗结束状态的行为"""
        print("[行为] 战斗结束 - 可以点击确认按钮返回")
        # 示例：点击确认按钮
        # 使用ClickManager执行点击
    
    def action_opening_chest(self):
        """开宝箱状态的行为"""
        print("[行为] 开宝箱中 - 可以点击开宝箱按钮")
        # 示例：点击开宝箱按钮
        # 使用ClickManager执行点击
    
    def action_other(self):
        """其他状态的行为"""
        print("[行为] 其他状态 - 无法识别的状态，跳过执行行为")
        # 示例：可以添加一些通用处理逻辑
    
    def process_screenshot(self, screenshot_path):
        """处理截图：识别状态并执行行为"""
        print(f"\n处理截图: {screenshot_path}")
        print("=" * 50)
        
        # 识别状态
        status, similarity = self.recognize_status(screenshot_path)
        
        if status:
            # 检查是否超过阈值
            threshold = self.status_templates[status]["threshold"]
            if similarity >= threshold:
                print(f"✓ 识别结果: {status} (相似度: {similarity:.4f})")
                # 执行对应行为
                self.execute_action(status)
            else:
                print(f"⚠ 识别结果（低置信度）: {status} (相似度: {similarity:.4f}，阈值: {threshold})")
                print(f"  建议：调整阈值或添加更多模板")
        else:
            print(f"✗ 无法识别状态 (最高相似度: {similarity:.4f})")
        
        print("=" * 50)

# 示例用法
def main():
    """示例：使用状态识别器"""
    print("屏幕状态识别器示例")
    print("=" * 30)
    
    # 创建状态识别器实例
    recognizer = ScreenStatusRecognizer()
    
    # 测试所有示例图片
    test_images = [
        "png/战斗未开始/初始页面.png",
        "png/战斗中/对战界面.png",
        "png/战斗结束/战斗结束页面.png",
        "png/开宝箱/开宝箱界面.png"
    ]
    
    for img_path in test_images:
        if os.path.exists(img_path):
            recognizer.process_screenshot(img_path)
        else:
            print(f"测试图片不存在: {img_path}")
    
    print("\n示例结束")

if __name__ == "__main__":
    main()