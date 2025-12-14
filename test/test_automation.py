#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试自动化工具的capture_and_analyze方法
"""

import sys
import os
# 将项目根目录添加到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cr.automation import CRGameAutomation

def main():
    # 创建自动化工具实例
    automation = CRGameAutomation()
    
    # 测试默认行为：不执行行为
    print("\n=== 测试1: 默认不执行行为 ===")
    status, screenshot_path = automation.capture_and_analyze(prefix="test_no_action")
    print(f"识别结果: {status}, 截图路径: {screenshot_path}")
    
    # 测试执行行为
    print("\n=== 测试2: 执行行为 ===")
    status, screenshot_path = automation.capture_and_analyze(prefix="test_with_action", execute_action=True)
    print(f"识别结果: {status}, 截图路径: {screenshot_path}")

if __name__ == "__main__":
    main()
