import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from check_clash_royale import extract_elixir

# 测试实际游戏截图
def test_actual_screenshots():
    # 实际游戏截图目录
    screenshots_dir = 'png/实际游戏截图/战斗中'
    
    print(f"\n=== 开始测试实际游戏截图中的圣水数量 ===")
    print(f"测试目录: {screenshots_dir}")
    
    # 获取目录下所有图片文件
    image_files = [f for f in os.listdir(screenshots_dir) if f.endswith('.png')]
    
    if not image_files:
        print("❌ 目录中没有PNG图片文件")
        return
    
    print(f"找到 {len(image_files)} 张PNG图片")
    
    # 测试前5张图片
    for i, image_file in enumerate(image_files[:5]):
        image_path = os.path.join(screenshots_dir, image_file)
        print(f"\n--- 测试第 {i+1} 张图片: {image_file} ---")
        
        # 调用extract_elixir函数
        elixir_amount, processed_file = extract_elixir(image_path)
        
        if elixir_amount is not None:
            print(f"✅ 图片 {image_file} 的圣水数量: {elixir_amount}")
        else:
            print(f"❌ 无法识别图片 {image_file} 的圣水数量")
    
    print(f"\n=== 实际游戏截图测试完成 ===")

if __name__ == "__main__":
    test_actual_screenshots()