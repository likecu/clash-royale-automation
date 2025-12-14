#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil

# 配置项
CLEAN_DIRS = [
    '/Volumes/600g/app1/皇室战争/png',
    '/Volumes/600g/app1/皇室战争/wechat_png'
]
DELETE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')  # 要删除的文件扩展名


def clean_directory(directory):
    """清理指定目录下的根级图片文件，保留子文件夹"""
    print(f"\n开始清理 {directory} 目录下的根级图片文件...")
    
    # 检查目录是否存在
    if not os.path.exists(directory):
        print(f"✗ 目录不存在: {directory}")
        return 0, 0
    
    # 获取目录下的所有文件和文件夹
    items = os.listdir(directory)
    
    # 统计信息
    deleted_count = 0
    total_size_deleted = 0
    
    for item in items:
        item_path = os.path.join(directory, item)
        
        # 检查是否为文件（不是文件夹）
        if os.path.isfile(item_path):
            # 检查是否为图片文件（可选：根据扩展名过滤）
            if item.lower().endswith(DELETE_EXTENSIONS):
                # 获取文件大小
                file_size = os.path.getsize(item_path)
                
                # 删除文件
                try:
                    os.remove(item_path)
                    deleted_count += 1
                    total_size_deleted += file_size
                    print(f"✓ 删除文件: {item} ({file_size / 1024:.1f} KB)")
                except Exception as e:
                    print(f"✗ 删除文件失败: {item} - {e}")
            else:
                print(f"✗ 跳过非图片文件: {item}")
        else:
            print(f"✓ 保留文件夹: {item}")
    
    return deleted_count, total_size_deleted


def main():
    """主函数，清理所有配置的目录"""
    print("=== 开始清理图片文件 ===")
    
    total_deleted = 0
    total_size = 0
    
    for directory in CLEAN_DIRS:
        deleted, size = clean_directory(directory)
        total_deleted += deleted
        total_size += size
    
    # 打印总体清理结果
    print(f"\n=== 总体清理完成 ===")
    print(f"删除的文件总数: {total_deleted}")
    print(f"释放的总空间: {total_size / (1024 * 1024):.2f} MB")
    print("======================")


if __name__ == "__main__":
    main()
