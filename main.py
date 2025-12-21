from cr import CRGameAutomation
import os

"""皇室战争游戏自动化工具主入口"""

def main():
    """主函数，演示皇室战争自动化工具的使用"""
    print("皇室战争游戏自动化工具")
    print("=" * 30)
    
    # 创建自动化工具实例（启用YOLO功能）
    cr_automation = CRGameAutomation(use_yolo=True)
    
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
    
    # 演示4: YOLO战斗分析功能
    print("\n4. YOLO战斗分析功能演示")
    
    # 查找战斗中的截图
    battle_screenshots = []
    battle_dir = "png/战斗中"
    if os.path.exists(battle_dir):
        for file in os.listdir(battle_dir):
            if file.endswith(".png") and not file.endswith("_detection.png"):
                battle_screenshots.append(os.path.join(battle_dir, file))
    
    if battle_screenshots:
        # 使用第一个战斗截图进行演示
        battle_screenshot = battle_screenshots[0]
        print(f"\n使用战斗截图: {battle_screenshot}")
        
        # 分析战斗截图并给出下兵建议
        best_position = cr_automation.analyze_battle_screenshot(battle_screenshot)
        if best_position:
            print(f"✓ 推荐下兵位置: {best_position}")
    else:
        print("✗ 未找到战斗中的截图，无法演示YOLO功能")
    
    print("\n演示完成！")
    print("\n使用方法:")
    print("- 执行 capture_and_analyze() 进行实时截图和智能分析")
    print("- 执行 batch_analyze_screenshots() 批量分析现有截图")
    print("- 执行 analyze_existing_screenshot() 分析指定截图")
    print("- 执行 mark_button_on_screenshot() 在截图上标记按钮")
    print("- 执行 mark_all_buttons() 标记所有场景的按钮")
    print("- 执行 verify_marked_buttons() 验证标记的按钮位置")
    print("- 执行 analyze_battle_screenshot() 分析战斗截图并给出下兵建议")
    print("- 执行 capture_battle_and_analyze() 实时捕获战斗画面并分析下兵位置")

if __name__ == "__main__":
    main()