import time
import os
import subprocess

# 配置信息
OCR_SCRIPT = "/Volumes/600g/app1/doubao获取/python/doubao_ocr.py"
PYTHON_PATH = "/Volumes/600g/app1/okx-py/bin/python3"

# 创建截图目录
if not os.path.exists('cr_check_png'):
    os.makedirs('cr_check_png')

# 1. 截取全屏或指定区域
def check_clash_royale():
    print("\n=== 开始检查皇室战争界面 ===")
    
    # 截取全屏
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f'cr_check_png/fullscreen_check_{timestamp}.png'
    print(f"1. 正在截取全屏，保存为: {filename}")
    # 使用screencapture命令截取全屏
    subprocess.run(["screencapture", filename], check=True, capture_output=True, text=True)
    
    # 2. 使用OCR识别是否为皇室战争界面
    print("2. 正在使用OCR识别是否为皇室战争界面...")
    ocr_command = f"{PYTHON_PATH} {OCR_SCRIPT} {filename} --question \"这是皇室战争游戏界面吗？用yes或no回答，不需要其他解释。\""
    
    result = subprocess.run(ocr_command, shell=True, capture_output=True, text=True)
    
    print("3. OCR识别结果:")
    print(result.stdout)
    
    # 4. 分析结果 - 只检查回答部分
    import re
    # 提取回答内容
    answer_match = re.search(r'回答:\s*(.+)', result.stdout)
    if answer_match:
        answer = answer_match.group(1).strip().lower()
        print(f"提取到回答: {answer}")
        if "yes" in answer:
            print("✅ 识别成功：当前屏幕显示的是皇室战争界面！")
            return True, filename
        elif "no" in answer:
            print("❌ 识别失败：当前屏幕不是皇室战争界面")
            return False, filename
        else:
            print("⚠ 识别结果不确定，需要人工确认")
            return None, filename
    else:
        print("⚠ 无法提取回答内容，需要人工确认")
        return None, filename

# 5. 同时也测试原始的截图区域
def test_original_region():
    print("\n=== 测试原始截图区域 ===")
    # 原始的WeApp区域配置
    weapp_region = (948, 31, 513, 955)
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f'cr_check_png/original_region_{timestamp}.png'
    print(f"1. 正在截取原始WeApp区域 {weapp_region}，保存为: {filename}")
    # 使用screencapture命令截取指定区域
    x, y, width, height = weapp_region
    subprocess.run(["screencapture", "-R", f"{x},{y},{width},{height}", filename], check=True, capture_output=True, text=True)
    
    # 使用OCR识别
    print("2. 正在使用OCR识别原始区域...")
    ocr_command = f"{PYTHON_PATH} {OCR_SCRIPT} {filename} --question \"这是皇室战争游戏界面吗？用yes或no回答，不需要其他解释。\""
    
    result = subprocess.run(ocr_command, shell=True, capture_output=True, text=True)
    
    print("3. OCR识别结果:")
    print(result.stdout)
    
    # 4. 分析结果 - 只检查回答部分
    import re
    # 提取回答内容
    answer_match = re.search(r'回答:\s*(.+)', result.stdout)
    if answer_match:
        answer = answer_match.group(1).strip().lower()
        print(f"提取到回答: {answer}")
        if "yes" in answer:
            print("✅ 原始区域识别成功：是皇室战争界面！")
            return True, filename
        elif "no" in answer:
            print("❌ 原始区域识别失败：不是皇室战争界面")
            return False, filename
        else:
            print("⚠ 原始区域识别结果不确定")
            return None, filename
    else:
        print("⚠ 无法提取回答内容，需要人工确认")
        return None, filename

# 主函数
if __name__ == "__main__":
    # 先检查全屏
    fullscreen_result, fullscreen_file = check_clash_royale()
    
    # 再检查原始区域
    original_result, original_file = test_original_region()
    
    print("\n=== 最终结果 ===")
    print(f"全屏检查结果: {'✅ 是皇室战争' if fullscreen_result else '❌ 不是皇室战争'}")
    print(f"原始区域检查结果: {'✅ 是皇室战争' if original_result else '❌ 不是皇室战争'}")
    
    if fullscreen_result and not original_result:
        print("⚠ 注意：全屏有皇室战争，但原始截图区域不对，需要调整截图区域！")
    elif not fullscreen_result:
        print("❌ 未检测到皇室战争界面，请确保游戏已打开并显示在屏幕上")
    else:
        print("✅ 成功检测到皇室战争界面！")
