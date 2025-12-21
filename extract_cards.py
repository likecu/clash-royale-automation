#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
皇室战争卡牌提取和OCR识别脚本
"""

import os
import sys
from PIL import Image
import shutil


def extract_cards_from_screenshot(screenshot_path, output_dir):
    """从截图中提取卡牌
    
    参数:
        screenshot_path: 战斗截图路径
        output_dir: 卡牌输出目录
    """
    print(f"\n=== 处理截图: {os.path.basename(screenshot_path)} ===")
    
    # 打开图片
    img = Image.open(screenshot_path)
    width, height = img.size
    
    # 定义卡牌区域（基于分析结果）
    card_area_height = int(height * 0.15)  # 底部15%为卡牌区域
    card_area_top = height - card_area_height
    card_area_bottom = height
    
    # 底部卡牌数量和间距（皇室战争通常有4-5张卡牌）
    card_count = 4
    card_width = int(width / card_count)
    card_padding = 10  # 卡牌之间的间距
    
    extracted_cards = []
    
    # 裁剪每张卡牌
    for i in range(card_count):
        # 计算卡牌坐标，添加适当间距
        card_x1 = i * card_width + card_padding
        card_x2 = (i + 1) * card_width - card_padding
        card_y1 = card_area_top + card_padding
        card_y2 = card_area_bottom - card_padding
        
        # 确保坐标在有效范围内
        card_x1 = max(0, card_x1)
        card_x2 = min(width, card_x2)
        card_y1 = max(0, card_y1)
        card_y2 = min(height, card_y2)
        
        # 裁剪卡牌
        card_img = img.crop((card_x1, card_y1, card_x2, card_y2))
        
        # 保存卡牌图片
        card_filename = f"card_{i+1}_{os.path.basename(screenshot_path)}"
        card_path = os.path.join(output_dir, card_filename)
        card_img.save(card_path)
        
        print(f"✓ 裁剪卡牌 {i+1}: {card_path}")
        extracted_cards.append(card_path)
    
    return extracted_cards


def ocr_recognize_card(card_path):
    """使用OCR识别卡牌内容（单线程执行）
    
    参数:
        card_path: 卡牌图片路径
        
    返回:
        ocr_result: OCR识别结果
    """
    print(f"\n=== OCR识别卡牌: {os.path.basename(card_path)} ===")
    
    # OCR工具路径
    ocr_script = "/Volumes/600g/app1/doubao获取/python/gemini_ocr.py"
    virtual_env_python = "/Users/aaa/python-sdk/python3.13.2/bin/python"
    
    try:
        # 步骤1: 询问是否只有一张皇室战争卡牌
        question1 = "这张图片中是不是只有一张皇室战争的卡牌？请用yes或no回答"
        ocr_command1 = f"{virtual_env_python} {ocr_script} {card_path} --question '{question1}'"
        
        print(f"执行命令1: {ocr_command1}")
        result1 = os.popen(ocr_command1).read()
        print(f"OCR结果1:\n{result1}")
        
        # 检查OCR是否返回结果
        if not result1 or "识别失败" in result1:
            return f"是否单张卡牌: 识别失败\n卡牌名称: 无法识别"
        
        # 步骤2: 如果是，询问卡牌名称
        if "yes" in result1.lower() or "是的" in result1:
            question2 = "请识别这张皇室战争卡牌的名称"
            ocr_command2 = f"{virtual_env_python} {ocr_script} {card_path} --question '{question2}'"
            
            print(f"执行命令2: {ocr_command2}")
            result2 = os.popen(ocr_command2).read()
            print(f"OCR结果2:\n{result2}")
            
            if not result2 or "识别失败" in result2:
                return f"是否单张卡牌: {result1.strip()}\n卡牌名称: 无法识别"
            
            return f"是否单张卡牌: {result1.strip()}\n卡牌名称: {result2.strip()}"
        else:
            return f"是否单张卡牌: {result1.strip()}\n识别失败: 不是单张皇室战争卡牌"
    except Exception as e:
        print(f"✗ OCR识别出错: {e}")
        return f"是否单张卡牌: 识别出错\n卡牌名称: {str(e)}"


def batch_process_screenshots(screenshot_dir, output_dir):
    """批量处理多张截图
    
    参数:
        screenshot_dir: 截图目录
        output_dir: 输出目录
    """
    print(f"\n=== 批量处理截图目录: {screenshot_dir} ===")
    
    # 获取目录中所有PNG图片
    screenshot_files = [f for f in os.listdir(screenshot_dir) if f.endswith(".png")]
    total_screenshots = len(screenshot_files)
    
    if total_screenshots == 0:
        print(f"✗ 在 {screenshot_dir} 中未找到PNG图片")
        return
    
    print(f"✓ 找到 {total_screenshots} 张PNG图片")
    
    # 处理每张截图
    for i, screenshot_file in enumerate(screenshot_files, 1):
        screenshot_path = os.path.join(screenshot_dir, screenshot_file)
        print(f"\n{'='*60}")
        print(f"处理截图 {i}/{total_screenshots}: {screenshot_file}")
        
        # 提取卡牌
        extracted_cards = extract_cards_from_screenshot(screenshot_path, output_dir)
        
        # 识别每张卡牌
        for card_path in extracted_cards:
            ocr_result = ocr_recognize_card(card_path)
            
            # 保存识别结果到文件
            result_file = card_path.replace(".png", "_ocr_result.txt")
            with open(result_file, "w", encoding="utf-8") as f:
                f.write(ocr_result)
            print(f"✓ OCR结果已保存: {result_file}")
    
    print(f"\n{'='*60}")
    print(f"✓ 所有截图处理完成！")


def main():
    """主函数"""
    print("皇室战争卡牌提取和OCR识别工具")
    print("=" * 50)
    
    # 检查参数
    if len(sys.argv) < 2:
        print("用法1: 单张图片处理")
        print("   python extract_cards.py <截图路径> [输出目录]")
        print("   示例: python extract_cards.py png/实际游戏截图/战斗中/战斗中.png")
        print("\n用法2: 批量处理目录下所有图片")
        print("   python extract_cards.py --batch <截图目录> [输出目录]")
        print("   示例: python extract_cards.py --batch png/实际游戏截图/战斗中")
        sys.exit(1)
    
    # 批量处理模式
    if sys.argv[1] == "--batch":
        if len(sys.argv) < 3:
            print("✗ 批量处理需要指定截图目录")
            print("用法: python extract_cards.py --batch <截图目录> [输出目录]")
            sys.exit(1)
        
        screenshot_dir = sys.argv[2]
        output_dir = sys.argv[3] if len(sys.argv) > 3 else "cards"
        
        # 检查目录是否存在
        if not os.path.exists(screenshot_dir):
            print(f"✗ 目录不存在: {screenshot_dir}")
            sys.exit(1)
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        print(f"✓ 输出目录: {output_dir}")
        
        # 批量处理
        batch_process_screenshots(screenshot_dir, output_dir)
    
    # 单张图片处理模式
    else:
        screenshot_path = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) > 2 else "cards"
        
        # 检查图片是否存在
        if not os.path.exists(screenshot_path):
            print(f"✗ 图片不存在: {screenshot_path}")
            sys.exit(1)
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        print(f"✓ 输出目录: {output_dir}")
        
        # 提取卡牌
        extracted_cards = extract_cards_from_screenshot(screenshot_path, output_dir)
        
        # OCR识别每张卡牌
        print("\n" + "=" * 50)
        print("开始OCR识别卡牌")
        
        for card_path in extracted_cards:
            ocr_result = ocr_recognize_card(card_path)
            
            # 保存识别结果到文件
            result_file = card_path.replace(".png", "_ocr_result.txt")
            with open(result_file, "w", encoding="utf-8") as f:
                f.write(ocr_result)
            print(f"✓ OCR结果已保存: {result_file}")
        
        print("\n" + "=" * 50)
        print(f"✓ 卡牌提取和OCR识别完成！")
        print(f"✓ 共处理 {len(extracted_cards)} 张卡牌")
        print(f"✓ 结果保存在: {output_dir}")


if __name__ == "__main__":
    main()
