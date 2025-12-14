from PIL import Image
import numpy as np
import os

class ScreenStatusRecognizer:
    """屏幕状态识别器，用于判断当前截图属于什么状态，并执行相应行为"""
    
    def __init__(self):
        self.status_templates = {
            "战斗未开始": {
                "template_path": "png/战斗未开始/",
                "threshold": 0.8,  # 匹配阈值，0-1之间，值越高匹配度要求越高
                "action": self.action_battle_not_started
            },
            "战斗中": {
                "template_path": "png/战斗中/",
                "threshold": 0.8,
                "action": self.action_battle_in_progress
            },
            "战斗结束": {
                "template_path": "png/战斗结束/",
                "threshold": 0.8,
                "action": self.action_battle_ended
            },
            "开宝箱": {
                "template_path": "png/开宝箱/",
                "threshold": 0.8,
                "action": self.action_opening_chest
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
                if "template_imgs" not in config:
                    continue
                
                # 获取该状态下的所有模板
                template_imgs = config["template_imgs"]
                status_max_similarity = 0
                
                # 遍历该状态下的所有模板
                for i, template in enumerate(template_imgs):
                    similarity = self.compare_images(screenshot, template)
                    print(f"状态比较: {status} -> 模板{i+1}/{len(template_imgs)} -> 相似度: {similarity:.4f}")
                    
                    # 更新该状态下的最高相似度
                    if similarity > status_max_similarity:
                        status_max_similarity = similarity
                
                print(f"状态比较: {status} -> 最高相似度: {status_max_similarity:.4f}")
                
                # 更新全局最佳匹配
                if status_max_similarity > best_similarity and status_max_similarity >= config["threshold"]:
                    best_similarity = status_max_similarity
                    best_status = status
            
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
    
    def process_screenshot(self, screenshot_path):
        """处理截图：识别状态并执行行为"""
        print(f"\n处理截图: {screenshot_path}")
        print("=" * 50)
        
        # 识别状态
        status, similarity = self.recognize_status(screenshot_path)
        
        if status:
            print(f"✓ 识别结果: {status} (相似度: {similarity:.4f})")
            # 执行对应行为
            self.execute_action(status)
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