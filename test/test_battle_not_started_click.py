#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试战斗未开始状态下的点击操作
"""

import sys
import os
# 将项目根目录添加到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cr.automation import CRGameAutomation


def test_battle_not_started_click():
    """测试战斗未开始状态下的点击操作"""
    print("=== 测试战斗未开始状态下的点击操作 ===")
    automation = CRGameAutomation()
    
    # 打印皇室战争窗口位置信息
    cr_window_pos = automation.action_executor.click_manager.get_cr_window_position()
    print(f"\n=== 皇室战争窗口信息 ===")
    print(f"左上角坐标: ({cr_window_pos['x']}, {cr_window_pos['y']})")
    print(f"窗口大小: {cr_window_pos['width']}x{cr_window_pos['height']}")
    print(f"右下角坐标: ({cr_window_pos['right']}, {cr_window_pos['bottom']})")
    
    # 捕获并分析屏幕，识别状态
    status, screenshot_path = automation.capture_and_analyze(prefix="test_click")
    
    if status == "战斗未开始":
        print(f"\n识别到状态: {status}")
        print("执行点击操作...")
        # 直接执行智能行为
        success = automation.execute_smart_action(status, screenshot_path)
        if success:
            print("✓ 点击操作执行成功")
        else:
            print("✗ 点击操作执行失败")
    else:
        print(f"\n未识别到'战斗未开始'状态，当前状态: {status}")
        print("跳过点击操作")


if __name__ == "__main__":
    test_battle_not_started_click()
