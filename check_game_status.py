#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查皇室战争游戏当前状态的脚本
"""

import time
from cr import CRGameAutomation
from config.config import BUTTON_CONFIG

def check_game_status():
    """检查游戏状态并推荐操作"""
    # 记录开始时间
    start_time = time.time()
    print("开始检查游戏状态...")
    print(f"开始时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 创建自动化实例
    auto = CRGameAutomation()
    
    # 捕获屏幕并分析状态
    status, screenshot_path = auto.capture_and_analyze()
    
    print(f"\n当前游戏状态: {status}")
    
    if status:
        # 获取该状态下的按钮配置
        buttons = BUTTON_CONFIG.get(status, {})
        if buttons:
            # 推荐第一个按钮
            recommended_button = list(buttons.keys())[0]
            print(f"推荐点击按钮: {recommended_button}")
            print(f"按钮位置: {buttons[recommended_button]}")
        else:
            print(f"该状态 '{status}' 下没有配置按钮")
    else:
        print("无法识别当前游戏状态")
    
    # 记录结束时间并计算总耗时
    end_time = time.time()
    total_time = end_time - start_time
    print(f"\n结束时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"总流程耗时: {total_time:.2f} 秒")

if __name__ == "__main__":
    check_game_status()
