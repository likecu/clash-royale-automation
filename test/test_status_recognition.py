#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试状态识别器的功能
"""

import sys
import os
# 将项目根目录添加到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import os
from cr.status_recognizer import StatusRecognizer
from test_utils import print_test_header, print_test_result

def main():
    # 创建状态识别器实例
    recognizer = StatusRecognizer()
    
    # 测试不同状态的截图
    test_screenshots = [
        "png/战斗未开始/初始页面.png",
        "png/战斗中/对战界面.png",
        "png/战斗结束/战斗结束页面.png",
        "png/开宝箱/开宝箱界面.png"
    ]
    
    print_test_header("测试状态识别器的功能")
    
    for screenshot_path in test_screenshots:
        if os.path.exists(screenshot_path):
            status, similarity = recognizer.process_screenshot(screenshot_path)
            print_test_result(
                test_name=screenshot_path,
                status=status,
                similarity=similarity
            )
        else:
            print(f"\n❌ 截图文件不存在: {screenshot_path}")

if __name__ == "__main__":
    main()
