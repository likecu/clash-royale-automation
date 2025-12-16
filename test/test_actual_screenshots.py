#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试实际游戏截图的状态识别
"""

import sys
import os
# 将项目根目录添加到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import os
from cr.status_recognizer import StatusRecognizer
from test_utils import print_test_header, print_test_result, get_screenshot_paths

def main():
    print_test_header("测试实际游戏截图的状态识别")
    
    # 创建状态识别器实例
    recognizer = StatusRecognizer()
    
    # 实际游戏截图目录
    screenshots_dir = "./png/实际游戏截图"
    
    # 获取所有截图文件
    screenshot_paths = get_screenshot_paths(screenshots_dir)
    
    # 测试每个截图
    for screenshot_path in screenshot_paths:
        screenshot_file = os.path.basename(screenshot_path)
        
        # 预期状态（从文件夹结构提取）
        expected_status = os.path.basename(os.path.dirname(screenshot_path))
        
        # 识别状态
        status, similarity = recognizer.process_screenshot(screenshot_path)
        
        print_test_result(
            test_name=screenshot_file,
            status=status,
            expected=expected_status,
            similarity=similarity
        )

if __name__ == "__main__":
    main()
