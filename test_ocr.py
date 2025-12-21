from cr.screenshot import ScreenshotManager

# 创建一个ScreenshotManager实例
screenshot_manager = ScreenshotManager()

# 使用一个现有的截图文件进行测试
test_screenshot = "png/实际游戏截图/战斗中/战斗中.png"

# 调用is_clash_royale_screen方法
print(f"正在测试OCR识别: {test_screenshot}")
is_cr_screen = screenshot_manager.is_clash_royale_screen(test_screenshot)

# 打印结果
print(f"测试图片是否为皇室战争界面: {is_cr_screen}")