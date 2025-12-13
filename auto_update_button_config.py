from PIL import Image
import os
import numpy as np
from config.config import BUTTON_CONFIG, BUTTON_MARK_CONFIG

class ButtonConfigUpdater:
    """自动更新按钮配置的工具"""
    
    def __init__(self):
        self.png_dir = BUTTON_MARK_CONFIG["png_dir"]
        self.scene_configs = BUTTON_MARK_CONFIG["scene_configs"]
        self.updated_config = BUTTON_CONFIG.copy()
    
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
    
    def calculate_button_center(self, button_x, button_y, button_img):
        """计算按钮的中心点"""
        button_w, button_h = button_img.size
        center_x = button_x + button_w / 2
        center_y = button_y + button_h / 2
        return (int(center_x), int(center_y))
    
    def update_button_config(self, scene):
        """更新指定场景的按钮配置"""
        if scene == "战斗中":
            print(f"跳过场景: {scene}")
            return
        
        config = self.scene_configs[scene]
        scene_dir = os.path.join(self.png_dir, scene)
        
        # 构建文件路径
        interface_path = os.path.join(scene_dir, config["interface"])
        button_path = os.path.join(scene_dir, config["button"])
        
        print(f"处理场景: {scene}")
        print(f"  界面图: {interface_path}")
        print(f"  按钮图: {button_path}")
        
        # 打开图片
        interface_img = Image.open(interface_path)
        button_img = Image.open(button_path)
        
        # 找到按钮位置
        button_x, button_y = self.find_button_position(interface_img, button_img)
        
        # 计算中心点
        center = self.calculate_button_center(button_x, button_y, button_img)
        
        # 获取按钮名称
        if scene == "战斗未开始":
            button_name = "对战按钮"
        elif scene == "战斗结束":
            button_name = "确认按钮"
        elif scene == "开宝箱":
            button_name = "开宝箱按钮"
        else:
            button_name = "未知按钮"
        
        print(f"  按钮位置: ({button_x}, {button_y})")
        print(f"  按钮尺寸: {button_img.size}")
        print(f"  中心点: {center}")
        
        # 更新配置
        self.updated_config[scene][button_name] = center
    
    def update_all_configs(self):
        """更新所有非战斗中场景的按钮配置"""
        print("开始更新按钮配置...")
        print("=" * 50)
        
        for scene in self.scene_configs:
            if scene != "战斗中":
                self.update_button_config(scene)
        
        print("=" * 50)
        print("按钮配置更新完成!")
        print("\n更新后的配置:")
        print("BUTTON_CONFIG = {")
        for scene, buttons in self.updated_config.items():
            print(f"    \"{scene}\": {{")
            for button_name, position in buttons.items():
                print(f"        \"{button_name}\": {position},")
            print(f"    }},")
        print("}")
    
    def write_config_to_file(self):
        """将更新后的配置写入文件"""
        config_path = "config/config.py"
        
        # 读取现有文件内容
        with open(config_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 找到BUTTON_CONFIG的开始和结束位置
        start_idx = None
        end_idx = None
        for i, line in enumerate(lines):
            if "BUTTON_CONFIG = {" in line:
                start_idx = i
            elif start_idx is not None and line.strip() == "}":
                end_idx = i
                break
        
        if start_idx is None or end_idx is None:
            print("\n无法找到BUTTON_CONFIG配置块")
            return
        
        # 构建新的BUTTON_CONFIG行
        new_lines = []
        new_lines.append("# 按钮位置配置\n")
        new_lines.append("BUTTON_CONFIG = {\n")
        for scene, buttons in self.updated_config.items():
            new_lines.append("    \"" + scene + "\": {\n")
            for button_name, position in buttons.items():
                new_lines.append("        \"" + button_name + "\": " + str(position) + ",  # 自动识别的位置\n")
            new_lines.append("    },\n")
        new_lines.append("}\n")
        
        # 替换原文件中的BUTTON_CONFIG部分
        updated_lines = lines[:start_idx] + new_lines + lines[end_idx+1:]
        
        # 写入更新后的内容
        with open(config_path, 'w', encoding='utf-8') as f:
            f.writelines(updated_lines)
        
        print(f"\n配置已写入文件: {config_path}")

def main():
    """主函数"""
    print("按钮配置自动更新工具")
    print("=" * 30)
    print("该工具将自动识别除战斗中外所有场景的按钮中心点，并更新配置文件")
    print()
    
    updater = ButtonConfigUpdater()
    updater.update_all_configs()
    
    # 直接写入文件，不询问用户
    updater.write_config_to_file()
    print("配置文件已更新!")
    
    print("\n所有操作完成")

if __name__ == "__main__":
    main()