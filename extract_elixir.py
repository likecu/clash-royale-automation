#!/usr/bin/env python3
import os
import subprocess
import sys
import json
import re

# 设置虚拟环境Python路径和OCR脚本路径
PYTHON_PATH = '/Users/aaa/python-sdk/python3.13.2/bin/python'
OCR_SCRIPT = '/Volumes/600g/app1/doubao获取/python/gemini_ocr.py'
IMAGE_DIR = '/Volumes/600g/app1/皇室战争/png/实际游戏截图/战斗中'
RESULT_FILE = '/Volumes/600g/app1/皇室战争/elixir_results.json'

# 从OCR结果中提取纯净的圣水数量
def extract_pure_elixir(ocr_result):
    # 查找回答部分
    answer_start = ocr_result.find('回答: ')
    if answer_start == -1:
        return 0
    
    answer = ocr_result[answer_start + 4:]
    
    # 尝试解析JSON格式的回答
    try:
        import json
        result = json.loads(answer)
        if isinstance(result, dict) and 'elixir_count' in result:
            elixir_count = result['elixir_count']
            if isinstance(elixir_count, int):
                return elixir_count
            # 如果是字符串类型的数字，尝试转换为整数
            elif isinstance(elixir_count, str) and elixir_count.isdigit():
                return int(elixir_count)
    except (json.JSONDecodeError, ValueError):
        # JSON解析失败，尝试使用正则表达式提取数字作为备选方案
        import re
        # 从回答中提取数字
        number_match = re.search(r'\b(\d+)\b', answer)
        if number_match:
            return int(number_match.group(1))
    
    # 如果所有方法都失败，返回默认值0
    return 0

# 识别单张图片的圣水数量
def process_single_image(image_path):
    filename = os.path.basename(image_path)
    print(f"\n处理图片: {filename}")
    # 调用OCR工具提取圣水数量
    try:
        result = subprocess.run(
            [PYTHON_PATH, OCR_SCRIPT, image_path, '--question', '图中的皇室战争游戏的当前拥有的圣水数量是多少？请输出标准JSON格式，键为elixir_count，值为整数类型的圣水数量，如果无法识别则值为0，例如：{"elixir_count": 10}'],
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
