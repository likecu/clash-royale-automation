#!/usr/bin/env python3
"""
测试脚本：测试状态识别器对所有实际游戏截图的识别效果
"""

import sys
import os
# 将项目根目录添加到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from cr.status_recognizer import StatusRecognizer
from test_utils import (
    get_screenshot_paths,
    get_expected_status_from_path,
    print_test_header,
    print_test_result,
    print_test_summary
)

def main():
    """主函数"""
    print_test_header("测试状态识别器对所有实际游戏截图的识别效果")
    
    # 创建状态识别器实例
    recognizer = StatusRecognizer()
    
    # 获取所有实际游戏截图
    screenshot_dir = "png/实际游戏截图/"
    screenshot_paths = get_screenshot_paths(screenshot_dir)
    
    # 统计结果
    total = 0
    correct = 0
    total_time = 0
    
    print(f"找到 {len(screenshot_paths)} 张测试图片")
    print("=" * 60)
    
    # 测试每张图片
    for screenshot_path in screenshot_paths:
        total += 1
        
        # 提取预期状态（从文件夹名或文件名推断）
        expected_status = get_expected_status_from_path(screenshot_path)
        
        # 记录开始时间
        start_time = time.time()
        
        # 识别状态
        status, similarity = recognizer.recognize_status(screenshot_path)
        
        # 记录结束时间
        end_time = time.time()
        elapsed = end_time - start_time
        total_time += elapsed
        
        # 检查是否正确识别
        is_correct = status == expected_status
        if is_correct:
            correct += 1
        
        print_test_result(
            test_name=screenshot_path,
            status=status,
            expected=expected_status,
            similarity=similarity,
            elapsed=elapsed
        )
    
    print_test_summary(total, correct, total_time)

if __name__ == "__main__":
    main()
