#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试实际游戏截图的状态识别
"""

import os
from cr.status_recognizer import StatusRecognizer

def main():
    # 创建状态识别器实例
    recognizer = StatusRecognizer()
    
    # 实际游戏截图目录
    screenshots_dir = "/Volumes/600g/app1/皇室战争/png/实际游戏截图"
    
    # 获取目录下的所有图片文件
    screenshot_files = [f for f in os.listdir(screenshots_dir) if f.endswith(".png")]
    
    # 测试每个截图
    for screenshot_file in screenshot_files:
        screenshot_path = os.path.join(screenshots_dir, screenshot_file)
        
        print(f"\n{'='*60}")
        print(f"测试实际游戏截图: {screenshot_file}")
        print(f"{'='*60}")
        
        # 预期状态（从文件名提取）
        expected_status = screenshot_file.split(".")[0]
        print(f"预期状态: {expected_status}")
        
        # 识别状态
        status, similarity = recognizer.process_screenshot(screenshot_path)
        
        # 验证结果
        if status == expected_status:
            print(f"✅ 识别成功！预期: {expected_status}, 实际: {status}, 相似度: {similarity:.4f}")
        else:
            print(f"❌ 识别失败！预期: {expected_status}, 实际: {status}, 相似度: {similarity:.4f}")

if __name__ == "__main__":
    main()
