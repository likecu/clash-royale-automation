#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量处理皇室战争战斗截图，使用YOLO识别并标注推荐位置
"""

import os
import sys
from cr import YoloDetector


def main():
    """主函数"""
    print("皇室战争战斗截图YOLO批量处理脚本")
    print("=" * 50)
    
    # 配置参数
    input_dir = "/Volumes/600g/app1/皇室战争/png/实际游戏截图/战斗中"
    output_dir = "/Volumes/600g/app1/皇室战争/yolo"
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 初始化YOLO检测器
    yolo = YoloDetector()
    
    # 获取所有PNG图片
    image_files = [f for f in os.listdir(input_dir) if f.endswith(".png")]
    total_files = len(image_files)
    
    if total_files == 0:
        print(f"✗ 在 {input_dir} 中未找到PNG图片")
        sys.exit(1)
    
    print(f"✓ 找到 {total_files} 张PNG图片，开始处理...")
    
    # 遍历处理所有图片
    for i, filename in enumerate(image_files, 1):
        image_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)
        
        print(f"\n[{i}/{total_files}] 处理: {filename}")
        
        # 使用YOLO检测并可视化
        best_position = yolo.detect_and_visualize(image_path, output_path)
        
        if best_position:
            print(f"✓ 推荐下兵位置: {best_position}")
        else:
            print(f"✗ 未检测到有效下兵位置")
    
    print(f"\n{'=' * 50}")
    print(f"✓ 所有图片处理完成！结果保存在: {output_dir}")


if __name__ == "__main__":
    main()
