#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
皇室战争YOLO检测测试脚本
"""

import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cr import YoloDetector


def main():
    """主函数"""
    print("皇室战争YOLO检测测试脚本")
    print("=" * 50)
    
    # 检查参数
    if len(sys.argv) < 2:
        print("用法: python test_yolo.py <截图路径> [输出路径]")
        print("示例: python test_yolo.py png/战斗中/战斗中.png")
        sys.exit(1)
    
    image_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    # 检查图片是否存在
    if not os.path.exists(image_path):
        print(f"✗ 图片不存在: {image_path}")
        sys.exit(1)
    
    # 初始化YOLO检测器
    yolo = YoloDetector()
    
    # 检测并可视化结果
    best_position = yolo.detect_and_visualize(image_path, output_path)
    
    if best_position:
        print(f"\n✓ 最佳下兵位置: {best_position}")
    else:
        print("✗ 未检测到有效下兵位置")


if __name__ == "__main__":
    main()
