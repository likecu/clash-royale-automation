#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试点击位置计算准确性的脚本
"""

import sys
import os
# 将项目根目录添加到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cr.action_executor import ActionExecutor
from cr.click_manager import ClickManager

def test_click_position():
    """测试点击位置计算"""
    print("=== 测试点击位置计算 ===")
    
    # 创建ActionExecutor实例
    executor = ActionExecutor()
    
    # 测试战斗结束状态的确认按钮
    button_pos = (1205, 882)  # 确认按钮的配置坐标
    print(f"\n测试按钮: 确认按钮")
    print(f"按钮配置坐标: {button_pos}")
    
    # 调用坐标转换方法
    actual_x, actual_y = executor._calculate_relative_position(button_pos)
    print(f"\n计算结果:")
    print(f"实际点击位置: ({actual_x}, {actual_y})")
    
    # 测试战斗未开始状态的对战按钮
    button_pos = (1205, 795)  # 对战按钮的配置坐标
    print(f"\n\n测试按钮: 对战按钮")
    print(f"按钮配置坐标: {button_pos}")
    
    # 调用坐标转换方法
    actual_x, actual_y = executor._calculate_relative_position(button_pos)
    print(f"\n计算结果:")
    print(f"实际点击位置: ({actual_x}, {actual_y})")
    
    # 测试开宝箱按钮
    button_pos = (1236, 928)  # 开宝箱按钮的配置坐标
    print(f"\n\n测试按钮: 开宝箱按钮")
    print(f"按钮配置坐标: {button_pos}")
    
    # 调用坐标转换方法
    actual_x, actual_y = executor._calculate_relative_position(button_pos)
    print(f"\n计算结果:")
    print(f"实际点击位置: ({actual_x}, {actual_y})")
    
    print("\n=== 点击位置测试完成 ===")

if __name__ == "__main__":
    test_click_position()
