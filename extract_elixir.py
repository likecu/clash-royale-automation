#!/usr/bin/env python3
import os
import subprocess
import sys
import json
import re

# 设置虚拟环境Python路径和OCR脚本路径
PYTHON_PATH = '/Volumes/600g/app1/okx-py/bin/python3'
OCR_SCRIPT = '/Volumes/600g/app1/doubao获取/python/doubao_ocr.py'
IMAGE_DIR = '/Volumes/600g/app1/皇室战争/png/实际游戏截图/战斗中'
RESULT_FILE = '/Volumes/600g/app1/皇室战争/elixir_results.json'

# 从OCR结果中提取纯净的圣水数量
def extract_pure_elixir(ocr_result):
    # 查找回答部分
    answer_start = ocr_result.find('回答: ')
    if answer_start == -1:
        return '未找到回答'
    
    answer = ocr_result[answer_start + 4:]
    
    # 使用正则表达式提取数字
    # 匹配多种不同的表述方式，简化正则表达式，避免引号转义问题
    patterns = [
        r'圣水数量是\s*(\d+)',
        r'圣水是\s*(\d+)',
        r'(\d+)\s*圣水',
        r'当前的圣水数量是\s*(\d+)',
        r'显示当前的圣水数量是\s*(\d+)',
        r'当前圣水数量是\s*(\d+)',
        r'当前圣水数量显示为\s*(\d+)',
        r'底部显示当前圣水数量是\s*(\d+)',
        r'底部显示当前的圣水数量是\s*(\d+)',
        r'数值是\s*(\d+)',
        r'当前圣水数量为\s*(\d+)',
        r'圣水数量为\s*(\d+)',
        r'显示的圣水数量是\s*(\d+)',
        r'底部的圣水显示区域显示当前圣水数量是\s*(\d+)',
        r'底部的圣水显示区域明确标注了当前圣水数量为\s*(\d+)',
        r'底部圣水显示区域的数值是\s*(\d+)',
        r'底部可以看到，当前圣水数量显示为\s*(\d+)',
        r'显示为\s*(\d+)',
        r'当前圣水\s*(\d+)',
        r'显示的数值是\s*(\d+)',
        r'显示为\s*(\d+)\s*，',
        r'显示为\s*(\d+)\s*\('
    ]
    
    for pattern in patterns:
        match = re.search(pattern, answer)
        if match:
            return match.group(1)
    
    return '未识别到圣水数量'

# 识别单张图片的圣水数量
def process_single_image(image_path):
    filename = os.path.basename(image_path)
    print(f"\n处理图片: {filename}")
    # 调用OCR工具提取圣水数量
    try:
        result = subprocess.run(
            [PYTHON_PATH, OCR_SCRIPT, image_path, '--question', '图中的圣水数量是多少？'],
            capture_output=True,
            text=True,
            check=True
        )
        ocr_result = result.stdout.strip()
        pure_elixir = extract_pure_elixir(ocr_result)
        print(f"完整OCR结果: {ocr_result[:100]}...")  # 只显示前100个字符
        print(f"提取的圣水数量: {pure_elixir}")
        return filename, {
            'full_result': ocr_result,
            'elixir_count': pure_elixir
        }
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip()
        print(f"处理失败: {error_msg[:100]}...")
        return filename, {
            'full_result': '',
            'elixir_count': f"处理失败: {error_msg[:50]}..."
        }
    except Exception as e:
        error_msg = str(e)
        print(f"发生错误: {error_msg}")
        return filename, {
            'full_result': '',
            'elixir_count': f"发生错误: {error_msg}"
        }

# 保存结果到JSON文件
def save_results(results):
    with open(RESULT_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n结果已保存到: {RESULT_FILE}")

# 遍历目录下的所有PNG图片
def process_all_images():
    results = {}
    for filename in os.listdir(IMAGE_DIR):
        if filename.lower().endswith('.png'):
            image_path = os.path.join(IMAGE_DIR, filename)
            filename, result = process_single_image(image_path)
            results[filename] = result
    save_results(results)
    return results

if __name__ == "__main__":
    # 如果提供了图片路径参数，则处理单张图片，否则处理所有图片
    if len(sys.argv) > 1:
        # 使用提供的图片路径
        image_path = sys.argv[1]
        filename, result = process_single_image(image_path)
        results = {filename: result}
        save_results(results)
    else:
        # 处理所有图片
        process_all_images()
