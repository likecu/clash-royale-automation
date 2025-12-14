#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试状态识别器的功能
"""

import os
from cr.status_recognizer import StatusRecognizer

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
    
    for screenshot_path in test_screenshots:
        if os.path.exists(screenshot_path):
            print(f"\n{'='*60}")
            print(f"测试截图: {screenshot_path}")
            print(f"{'='*60}")
            status, similarity = recognizer.process_screenshot(screenshot_path)
        else:
            print(f"\n❌ 截图文件不存在: {screenshot_path}")

if __name__ == "__main__":
    main()
