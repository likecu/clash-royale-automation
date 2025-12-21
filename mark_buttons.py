from PIL import Image, ImageDraw, ImageEnhance, ImageChops
import os
import numpy as np

class ButtonMarker:
    """按钮标记器，用于在界面中标记按钮位置"""
    
    def __init__(self):
        self.png_dir = "png"
        self.scenes = [
            "战斗未开始",
            "战斗中",
            "战斗结束", 
            "开宝箱"
        ]
        self.scene_configs = {
            "战斗未开始": {
                "interface": "初始页面.png",
                "button": "对战按钮.png",
                "output": "初始页面_标记按钮.png"
            },
            "战斗中": {
                "interface": "对战界面.png",
                "button": "表情按钮.png",
                "output": "对战界面_标记按钮.png"
            },
            "战斗结束": {
                "interface": "战斗结束页面.png",
                "button": "战斗结束确认按钮.png",
                "output": "战斗结束页面_标记按钮.png"
            },
            "开宝箱": {
                "interface": "开宝箱界面.png",
                "button": "开宝箱界面按钮.png",
                "output": "开宝箱界面_标记按钮.png"
            }
        }
    
    def find_button_position(self, interface_img, button_img):
        """使用模板匹配找到按钮在界面中的位置"""
        # 将图片转换为numpy数组
        interface_np = np.array(interface_img)
        button_np = np.array(button_img)
        
        # 获取界面和按钮的尺寸
        interface_h, interface_w, _ = interface_np.shape
        button_h, button_w, _ = button_np.shape
        
        # 计算需要遍历的区域
        h_search = interface_h - button_h
        w_search = interface_w - button_w
        
        best_match = (0, 0)
        min_diff = float('inf')
        
        # 遍历界面，寻找与按钮最匹配的区域
        for y in range(0, h_search, 5):  # 步长为5，加快搜索速度
            for x in range(0, w_search, 5):
                # 截取当前区域
                region = interface_np[y:y+button_h, x:x+button_w, :]
                # 计算与按钮的差异
                diff = np.sum(np.abs(region - button_np))
                # 更新最佳匹配
                if diff < min_diff:
                    min_diff = diff
                    best_match = (x, y)
        
        return best_match
    
    def mark_button(self, scene):
        """标记指定场景的按钮位置"""
        config = self.scene_configs[scene]
        scene_dir = os.path.join(self.png_dir, scene)
        
        # 构建文件路径
        interface_path = os.path.join(scene_dir, config["interface"])
        button_path = os.path.join(scene_dir, config["button"])
        output_path = os.path.join(scene_dir, config["output"])
        
        print(f"处理场景: {scene}")
        print(f"  界面图: {interface_path}")
        print(f"  按钮图: {button_path}")
        
        # 打开图片
        interface_img = Image.open(interface_path)
        button_img = Image.open(button_path)
        
        # 找到按钮位置
        button_x, button_y = self.find_button_position(interface_img, button_img)
        
        # 在界面图上标记按钮位置
        draw = ImageDraw.Draw(interface_img)
        button_w, button_h = button_img.size
        
        # 绘制红色边框（3像素宽）
        outline_color = (255, 0, 0)
        outline_width = 3
        for i in range(outline_width):
            draw.rectangle([
                (button_x - i, button_y - i),
                (button_x + button_w + i, button_y + button_h + i)
            ], outline=outline_color)
        
        # 保存标记后的图片
        interface_img.save(output_path)
        print(f"  标记完成，保存为: {output_path}")
        
        return output_path
    
    def mark_all_buttons(self):
        """标记所有场景的按钮位置"""
        print("开始标记所有场景的按钮位置...")
        print("=" * 50)
        
        marked_files = []
        for scene in self.scenes:
            marked_file = self.mark_button(scene)
            marked_files.append(marked_file)
        
        print("=" * 50)
        print(f"✓ 所有场景的按钮标记完成，共生成 {len(marked_files)} 个标记文件")
        
        return marked_files
    
    def verify_with_doubao(self, image_path):
        """使用豆包验证按钮位置是否正确"""
        # 使用用户提供的OCR工具调用豆包
        ocr_cmd = f"/Users/aaa/python-sdk/python3.13.2/bin/python /Volumes/600g/app1/doubao获取/python/gemini_ocr.py {image_path} --question '图片中红色边框标记的位置是否是按钮？请回答是或否。'"
        
        print(f"\n调用豆包验证: {image_path}")
        print(f"执行命令: {ocr_cmd}")
        
        result = os.popen(ocr_cmd).read().strip()
        print(f"豆包返回结果: {result}")
        
        return result
    
    def verify_all_marked_files(self, marked_files):
        """验证所有标记文件"""
        print("\n开始验证所有标记文件...")
        print("=" * 50)
        
        results = []
        for file_path in marked_files:
            result = self.verify_with_doubao(file_path)
            results.append((file_path, result))
        
        print("=" * 50)
        print("验证结果汇总:")
        for file_path, result in results:
            print(f"{os.path.basename(file_path)}: {result}")
        
        return results

def main():
    """主函数"""
    print("按钮自动标记与验证工具")
    print("=" * 30)
    
    marker = ButtonMarker()
    
    # 标记所有按钮
    marked_files = marker.mark_all_buttons()
    
    # 验证所有标记文件
    results = marker.verify_all_marked_files(marked_files)
    
    print("\n所有操作完成")

if __name__ == "__main__":
    main()