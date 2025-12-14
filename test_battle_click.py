#!/usr/bin/env python3
# 皇室战争战斗中按钮点击测试脚本

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cr.automation import CRGameAutomation


def test_battle_click():
    """测试战斗中按钮点击功能"""
    print("=== 皇室战争战斗中按钮点击测试 ===")
    
    # 初始化自动化工具
    automation = CRGameAutomation()
    
    try:
        # 1. 捕获并分析当前屏幕状态
        print("\n1. 捕获并分析当前屏幕状态...")
        status, screenshot_path = automation.capture_and_analyze(execute_action=False)
        
        if not status:
            print("无法识别当前状态，测试结束")
            return
        
        # 2. 如果当前不是战斗中状态，询问是否继续测试
        if status != "战斗中":
            print(f"当前状态为: {status}，不是战斗中状态")
            # confirm = input("是否要直接测试战斗中按钮点击功能？(y/n): ")
            # if confirm.lower() != 'y':
            #     print("测试结束")
            #     return
        
        # 3. 执行战斗中按钮点击序列
        print("\n2. 执行战斗中按钮点击序列...")
        automation.action_executor.action_battle_in_progress()
        
        print("\n=== 测试完成 ===")
        
    except KeyboardInterrupt:
        print("\n测试被用户中断")
    except Exception as e:
        print(f"\n测试出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_battle_click()
