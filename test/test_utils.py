#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试工具模块，包含测试中使用的公用方法
"""

import sys
import os
# 将项目根目录添加到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import os
import time

def create_test_instance(class_path, *args, **kwargs):
    """
    创建测试实例
    
    参数:
        class_path: 类的完整路径，如 "cr.status_recognizer.StatusRecognizer"
        *args: 类初始化参数
        **kwargs: 类初始化关键字参数
    
    返回:
        类实例
    """
    try:
        module_path, class_name = class_path.rsplit('.', 1)
        module = __import__(module_path, fromlist=[class_name])
        cls = getattr(module, class_name)
        return cls(*args, **kwargs)
    except Exception as e:
        print(f"✗ 创建实例失败: {e}")
        return None

def get_screenshot_paths(base_dir="png", file_ext=".png"):
    """
    获取指定目录下所有截图路径
    
    参数:
        base_dir: 基础目录
        file_ext: 文件扩展名
    
    返回:
        截图路径列表
    """
    screenshot_paths = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(file_ext):
                full_path = os.path.join(root, file)
                screenshot_paths.append(full_path)
    screenshot_paths.sort()
    return screenshot_paths

def get_expected_status_from_path(screenshot_path):
    """
    从路径中推断预期状态
    
    参数:
        screenshot_path: 截图路径
    
    返回:
        预期状态字符串
    """
    if "战斗未开始" in screenshot_path:
        return "战斗未开始"
    elif "战斗中" in screenshot_path:
        return "战斗中"
    elif "战斗结束" in screenshot_path:
        return "战斗结束"
    elif "开宝箱" in screenshot_path:
        return "开宝箱"
    else:
        return "其他"

def print_test_header(title):
    """
    打印测试标题
    
    参数:
        title: 测试标题
    """
    print(f"\n{'='*60}")
    print(title)
    print(f"{'='*60}")

def print_test_result(test_name, status, expected=None, similarity=None, elapsed=None):
    """
    打印测试结果
    
    参数:
        test_name: 测试名称
        status: 实际状态
        expected: 预期状态
        similarity: 相似度
        elapsed: 耗时
    """
    print(f"\n测试: {test_name}")
    print(f"识别结果: {status if status else '无法识别'}")
    
    if expected:
        is_correct = status == expected
        result = "✓ 正确" if is_correct else "✗ 错误"
        print(f"预期结果: {expected}")
        print(f"测试结果: {result}")
    
    if similarity is not None:
        print(f"相似度: {similarity:.4f}")
    
    if elapsed is not None:
        print(f"耗时: {elapsed:.3f} 秒")

def print_test_summary(total, correct, total_time):
    """
    打印测试总结
    
    参数:
        total: 总测试数
        correct: 正确数
        total_time: 总耗时
    """
    print(f"\n{'='*60}")
    print("测试总结")
    print(f"{'='*60}")
    print(f"测试总数: {total}")
    print(f"正确识别: {correct}")
    print(f"识别准确率: {correct / total * 100:.2f}%")
    print(f"平均识别时间: {total_time / total:.3f} 秒/张")
    print(f"总识别时间: {total_time:.2f} 秒")
    print(f"{'='*60}")

def get_cr_window_region(click_manager):
    """
    获取皇室战争窗口区域
    
    参数:
        click_manager: ClickManager实例
    
    返回:
        窗口区域字典
    """
    try:
        click_manager.update_cr_window_region()
        cr_window = click_manager.get_cr_window_position()
        print(f"✓ 成功获取皇室战争窗口区域: ({cr_window['x']}, {cr_window['y']}, {cr_window['width']}, {cr_window['height']})")
        return cr_window
    except Exception as e:
        print(f"✗ 自动获取窗口区域失败: {e}")
        return None

def manual_input_window_region():
    """
    手动输入窗口区域
    
    返回:
        窗口区域字典
    """
    try:
        x = int(input("请输入窗口左上角X坐标: "))
        y = int(input("请输入窗口左上角Y坐标: "))
        width = int(input("请输入窗口宽度: "))
        height = int(input("请输入窗口高度: "))
        
        cr_window = {
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "right": x + width,
            "bottom": y + height
        }
        print(f"✓ 手动设置窗口区域成功: ({x}, {y}, {width}, {height})")
        return cr_window
    except ValueError:
        print("✗ 输入无效")
        return None
