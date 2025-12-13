from cr import CRGameAutomation
import os

"""皇室战争游戏自动化工具主入口"""

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
    print("- 执行 mark_all_buttons() 标记所有场景的按钮")
    print("- 执行 verify_marked_buttons() 验证标记的按钮位置")

if __name__ == "__main__":
    main()