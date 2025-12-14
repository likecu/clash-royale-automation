#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试截图性能的脚本
"""

import time
from cr.automation import CRGameAutomation


def test_single_screenshot():
    """测试单次截图性能"""
    print("=== 测试单次截图性能 ===")
    automation = CRGameAutomation()
    
    start_time = time.time()
    status, screenshot_path = automation.capture_and_analyze(prefix="test_single")
    end_time = time.time()
    
    if screenshot_path:
        print(f"单次截图耗时: {end_time - start_time:.3f}秒")
        return end_time - start_time
    else:
        print("单次截图失败")
        return None


def test_continuous_screenshots(count=5):
    """测试连续截图性能"""
    print(f"\n=== 测试连续 {count} 次截图性能 ===")
    automation = CRGameAutomation()
    
    total_time = 0
    
    # 第一次截图需要完整流程
    start_time = time.time()
    status, screenshot_path = automation.capture_and_analyze(prefix="test_continuous_0")
    end_time = time.time()
    
    if screenshot_path:
        first_time = end_time - start_time
        total_time += first_time
        print(f"第 1 次截图耗时: {first_time:.3f}秒")
    else:
        print("第 1 次截图失败，无法继续测试")
        return None
    
    # 后续截图使用优化后的方法，跳过前置操作
    for i in range(1, count):
        start_time = time.time()
        status, screenshot_path = automation.capture_and_analyze(
            prefix=f"test_continuous_{i}", 
            skip_bring_to_front=True
        )
        end_time = time.time()
        
        if screenshot_path:
            current_time = end_time - start_time
            total_time += current_time
            print(f"第 {i+1} 次截图耗时: {current_time:.3f}秒")
        else:
            print(f"第 {i+1} 次截图失败")
    
    avg_time = total_time / count
    print(f"\n连续 {count} 次截图总耗时: {total_time:.3f}秒")
    print(f"平均每次截图耗时: {avg_time:.3f}秒")
    return avg_time


def test_batch_screenshot_method():
    """测试批量截图方法的性能"""
    print("\n=== 测试批量截图方法性能 ===")
    from cr.screenshot import ScreenshotManager
    
    screenshot_manager = ScreenshotManager()
    
    start_time = time.time()
    screenshots = screenshot_manager.batch_screenshot_weapp(count=3, interval=1)
    end_time = time.time()
    
    if screenshots:
        print(f"批量截图耗时: {end_time - start_time:.3f}秒")
        return end_time - start_time
    else:
        print("批量截图失败")
        return None


if __name__ == "__main__":
    print("皇室战争截图性能测试")
    print("=" * 30)
    
    # 测试单次截图
    single_time = test_single_screenshot()
    
    # 测试连续截图
    continuous_avg_time = test_continuous_screenshots(count=5)
    
    # 测试批量截图
    batch_time = test_batch_screenshot_method()
    
    print("\n" + "=" * 30)
    print("性能测试结果汇总:")
    if single_time:
        print(f"单次截图: {single_time:.3f}秒")
    if continuous_avg_time:
        print(f"连续5次截图平均: {continuous_avg_time:.3f}秒")
    if batch_time:
        print(f"批量3次截图总耗时: {batch_time:.3f}秒")
    print("=" * 30)
