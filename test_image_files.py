from PIL import Image
import os
from screenshot import AutoScreenshotManager

class AutoScreenshotTester:
    """自动截图测试器"""
    
    def __init__(self):
        self.existing_test_images = [
            "初始页面.png",
            "对战按钮.png",
            "表情按钮.png",
            "战斗结束确认按钮.png",
            "开宝箱界面-问号数量.png"
        ]
    
    def test_image_file(self, image_path):
        """测试图片文件是否可用"""
        try:
            print(f"测试图片文件: {image_path}")
            
            # 检查文件是否存在
            if not os.path.exists(image_path):
                print(f"✗ 文件不存在: {image_path}")
                return False
            
            # 检查文件大小
            file_size = os.path.getsize(image_path)
            if file_size == 0:
                print(f"✗ 文件为空: {image_path}")
                return False
            
            # 尝试打开图片
            with Image.open(image_path) as img:
                width, height = img.size
                print(f"✓ 图片 {image_path} 可用，尺寸: {width}x{height}，大小: {file_size} 字节")
                return True
                
        except Exception as e:
            print(f"✗ 处理图片 {image_path} 失败: {e}")
            return False
    
    def test_existing_images(self):
        """测试现有的图片文件"""
        print("开始测试现有图片文件...")
        print("=" * 50)
        
        results = []
        for image in self.existing_test_images:
            result = self.test_image_file(image)
            results.append((image, result))
        
        print("=" * 50)
        print("测试结果汇总:")
        for image, result in results:
            status = "✓ 成功" if result else "✗ 失败"
            print(f"{image}: {status}")
        
        success_count = sum(1 for _, result in results if result)
        print(f"\n总体结果: {success_count}/{len(self.existing_test_images)} 张图片文件可用")
        
        return success_count, len(self.existing_test_images)
    
    def test_auto_screenshot_functionality(self):
        """测试自动截图功能"""
        print("\n开始测试自动截图功能...")
        print("=" * 50)
        
        # 创建自动截图管理器
        screenshot_manager = AutoScreenshotManager()
        
        # 测试自动截取WeApp界面
        print("\n1. 测试自动截取WeApp界面")
        auto_screenshot = screenshot_manager.auto_screenshot_weapp()
        if auto_screenshot and self.test_image_file(auto_screenshot):
            print("✓ 自动WeApp截图测试通过")
            return True
        else:
            print("✗ 自动WeApp截图测试失败")
            return False

# 主测试函数
def main():
    """主函数，测试自动截图功能"""
    print("自动截图功能测试")
    print("=" * 30)
    
    tester = AutoScreenshotTester()
    
    # 测试现有图片
    tester.test_existing_images()
    
    # 测试自动截图功能
    tester.test_auto_screenshot_functionality()
    
    print("\n测试完成")

if __name__ == "__main__":
    main()
