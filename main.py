from screenshot import AutoScreenshotManager
from status_recognizer import ScreenStatusRecognizer
from PIL import Image, ImageDraw
import os
import pyautogui

class CRGameAutomation:
    """皇室战争游戏自动化工具，整合截图和状态识别功能"""
    
    def __init__(self):
        # 初始化截图管理器
        self.screenshot_manager = AutoScreenshotManager()
        # 初始化状态识别器
        self.status_recognizer = ScreenStatusRecognizer()
        # 按钮位置配置
        self.button_positions = {
            "战斗未开始": {
                "对战按钮": (1200, 850)  # 示例位置，需要根据实际情况调整
            },
            "战斗中": {
                "表情按钮": (1350, 850)  # 示例位置
            },
            "战斗结束": {
                "确认按钮": (1200, 700)  # 示例位置
            },
            "开宝箱": {
                "开宝箱按钮": (1200, 750)  # 示例位置
            }
        }
    
    def capture_and_analyze(self, prefix="weapp_auto"):
        """截取屏幕并分析状态，执行相应行为"""
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
            # 3. 执行相应行为
            self.execute_smart_action(status, screenshot_path)
        else:
            print(f"✗ 无法识别状态 (最高相似度: {similarity:.4f})")
        
        print("===== 捕获分析完成 =====")
        return status, screenshot_path
    
    def execute_smart_action(self, status, screenshot_path):
        """根据状态执行智能行为"""
        print(f"\n执行智能行为: {status}")
        
        # 根据状态执行不同的行为
        if status == "战斗未开始":
            self.start_battle()
        elif status == "战斗中":
            self.handle_battle()
        elif status == "战斗结束":
            self.end_battle()
        elif status == "开宝箱":
            self.open_chest()
        else:
            print(f"未知状态: {status}")
    
    def start_battle(self):
        """开始战斗"""
        print("[智能行为] 开始战斗 - 点击对战按钮")
        # 模拟点击对战按钮
        button_pos = self.button_positions["战斗未开始"]["对战按钮"]
        print(f"  点击位置: {button_pos}")
        # pyautogui.click(button_pos[0], button_pos[1])  # 取消注释以执行实际点击
    
    def handle_battle(self):
        """处理战斗中状态"""
        print("[智能行为] 战斗进行中 - 可以执行战斗操作")
        # 这里可以添加战斗中的智能操作
        # 例如：自动发送表情、使用卡牌等
    
    def end_battle(self):
        """结束战斗"""
        print("[智能行为] 战斗结束 - 点击确认按钮")
        # 模拟点击确认按钮
        button_pos = self.button_positions["战斗结束"]["确认按钮"]
        print(f"  点击位置: {button_pos}")
        # pyautogui.click(button_pos[0], button_pos[1])  # 取消注释以执行实际点击
    
    def open_chest(self):
        """开宝箱"""
        print("[智能行为] 开宝箱 - 点击开宝箱按钮")
        # 模拟点击开宝箱按钮
        button_pos = self.button_positions["开宝箱"]["开宝箱按钮"]
        print(f"  点击位置: {button_pos}")
        # pyautogui.click(button_pos[0], button_pos[1])  # 取消注释以执行实际点击
    
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

def main():
    """主函数，演示皇室战争自动化工具的使用"""
    print("皇室战争游戏自动化工具")
    print("=" * 30)
    
    # 创建自动化工具实例
    cr_automation = CRGameAutomation()
    
    # 演示1: 批量分析现有截图
    print("\n1. 批量分析现有截图")
    cr_automation.batch_analyze_screenshots("png")
    
    # 演示2: 分析指定截图
    print("\n2. 分析指定截图")
    test_screenshot = "png/战斗未开始/初始页面.png"
    if os.path.exists(test_screenshot):
        cr_automation.analyze_existing_screenshot(test_screenshot)
    
    # 演示3: 在截图上标记按钮
    print("\n3. 在截图上标记按钮")
    cr_automation.mark_button_on_screenshot(test_screenshot, "战斗未开始")
    
    print("\n演示完成！")
    print("\n使用方法:")
    print("- 执行 capture_and_analyze() 进行实时截图和智能分析")
    print("- 执行 batch_analyze_screenshots() 批量分析现有截图")
    print("- 执行 analyze_existing_screenshot() 分析指定截图")
    print("- 执行 mark_button_on_screenshot() 在截图上标记按钮")

if __name__ == "__main__":
    main()