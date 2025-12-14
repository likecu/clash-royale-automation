#!/usr/bin/env python3
"""
测试脚本：测试状态识别器对所有实际游戏截图的识别效果
"""

import os
import sys
import time
from status_recognizer import ScreenStatusRecognizer

def main():
    """主函数"""
    print("测试状态识别器对所有实际游戏截图的识别效果")
    print("=" * 60)
    
    # 创建状态识别器实例
    recognizer = ScreenStatusRecognizer()
    
    # 获取所有实际游戏截图
    screenshot_dir = "/Volumes/600g/app1/皇室战争/png/实际游戏截图/"
    screenshot_paths = []
    
    for root, dirs, files in os.walk(screenshot_dir):
        for file in files:
            if file.endswith('.png'):
                full_path = os.path.join(root, file)
                screenshot_paths.append(full_path)
    
    # 按路径排序
    screenshot_paths.sort()
    
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
        expected_status = ""
        if "战斗未开始" in screenshot_path:
            expected_status = "战斗未开始"
        elif "战斗中" in screenshot_path:
            expected_status = "战斗中"
        elif "战斗结束" in screenshot_path:
            expected_status = "战斗结束"
        elif "开宝箱" in screenshot_path:
            expected_status = "开宝箱"
        else:
            expected_status = "其他"
        
        print(f"\n测试图片: {screenshot_path}")
        print(f"预期状态: {expected_status}")
        
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
            result = "✓ 正确"
        else:
            result = "✗ 错误"
        
        print(f"识别结果: {status if status else '无法识别'} (相似度: {similarity:.4f})")
        print(f"识别时间: {elapsed:.3f} 秒")
        print(f"识别结果: {result}")
    
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"测试图片总数: {total}")
    print(f"正确识别数: {correct}")
    print(f"识别准确率: {correct / total * 100:.2f}%")
    print(f"平均识别时间: {total_time / total:.3f} 秒/张")
    print(f"总识别时间: {total_time:.2f} 秒")
    print("=" * 60)

if __name__ == "__main__":
    main()
