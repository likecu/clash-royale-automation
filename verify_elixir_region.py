import os
from PIL import Image

# 用于手动验证圣水区域的正确性
def verify_elixir_region():
    print("\n=== 开始验证圣水区域 ===")
    
    # 实际游戏截图目录
    screenshots_dir = '/Volumes/600g/app1/皇室战争/png/实际游戏截图/战斗中'
    
    # 获取目录下所有图片文件
    image_files = [f for f in os.listdir(screenshots_dir) if f.endswith('.png')]
    
    if not image_files:
        print("❌ 目录中没有PNG图片文件")
        return
    
    print(f"找到 {len(image_files)} 张PNG图片")
    
    # 选择第一张图片进行验证
    image_file = image_files[0]
    image_path = os.path.join(screenshots_dir, image_file)
    print(f"\n使用图片：{image_file}")
    
    # 打开图片
    img = Image.open(image_path)
    print(f"图片原始尺寸：{img.size}")
    
    # 圣水区域配置
    # 根据用户提供的信息：截图中(108, 625)坐标的地方有数字1-10，截图大小为335x640
    elixir_left = 108
    elixir_top = 625
    elixir_width = 335
    elixir_height = 640
    
    # 计算右下角坐标
    elixir_right = elixir_left + elixir_width
    elixir_bottom = elixir_top + elixir_height
    
    print(f"\n圣水区域配置：")
    print(f"- 左上角坐标：({elixir_left}, {elixir_top})")
    print(f"- 宽度：{elixir_width}，高度：{elixir_height}")
    print(f"- 右下角坐标：({elixir_right}, {elixir_bottom})")
    
    # 检查区域是否超出图片范围
    img_width, img_height = img.size
    if elixir_right > img_width or elixir_bottom > img_height:
        print(f"\n⚠ 警告：圣水区域超出图片范围！")
        print(f"- 图片尺寸：{img.size}")
        print(f"- 圣水区域右下角：({elixir_right}, {elixir_bottom})")
        return
    
    # 裁剪圣水区域
    elixir_region = (elixir_left, elixir_top, elixir_right, elixir_bottom)
    elixir_img = img.crop(elixir_region)
    
    # 保存裁剪后的图片
    output_dir = 'cr_check_png'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_path = os.path.join(output_dir, f'elixir_verify_{image_file}')
    elixir_img.save(output_path)
    
    print(f"\n✅ 圣水区域裁剪成功！")
    print(f"- 裁剪后图片尺寸：{elixir_img.size}")
    print(f"- 保存路径：{output_path}")
    print(f"\n请打开 {output_path} 查看裁剪后的圣水区域，确认是否包含数字1-10。")
    print("如果裁剪区域不正确，请调整代码中的elixir_left和elixir_top参数。")

if __name__ == "__main__":
    verify_elixir_region()