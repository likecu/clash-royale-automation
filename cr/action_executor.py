import subprocess
import time
from config.config import BUTTON_CONFIG
from cr.click_manager import ClickManager

class ActionExecutor:
    """操作执行器，根据状态执行相应的操作"""
    
    def __init__(self):
        self.button_positions = BUTTON_CONFIG
        # 初始化点击管理器
        self.click_manager = ClickManager()
        # 定义状态到操作方法的映射
        self.action_map = {
            "战斗未开始": self.action_battle_not_started,
            "战斗中": self.action_battle_in_progress,
            "战斗结束": self.action_battle_ended,
            "开宝箱": self.action_opening_chest
        }
    
    def execute_action(self, status):
        """根据状态执行相应的操作"""
        if status is None:
            print("无法识别状态，跳过执行行为")
            return False
        
        if status in self.action_map:
            print(f"\n执行状态行为: {status}")
            return self.action_map[status]()
        else:
            print(f"未知状态: {status}，无对应行为")
            return False
    
    def click_with_cliclick(self, x, y):
        """使用ClickManager执行点击操作"""
        return self.click_manager.click(x, y)
    
    def _calculate_relative_position(self, button_pos):
        """将按钮的绝对坐标转换为相对于当前皇室战争窗口的坐标"""
        # 获取当前皇室战争小程序窗口的位置
        cr_window_pos = self.click_manager.get_cr_window_position()
        print(f"  当前窗口位置: {cr_window_pos}")
        
        # 从配置文件注释理解坐标计算方式
        # 注释格式: (按钮在截图中的相对位置x*0.5+基准窗口x=按钮配置x, 按钮在截图中的相对位置y*0.5+基准窗口y=按钮配置y)
        # 例如: (514*0.5+948=1205, 1701*0.5+31=882)
        
        # 基准配置参数
        base_window_x = 948  # 基准窗口左上角x坐标
        base_window_y = 31    # 基准窗口左上角y坐标
        
        # 截图尺寸（从注释中反推）
        screenshot_width = 1028  # 因为 514*2 = 1028
        screenshot_height = 3402  # 因为 1701*2 = 3402
        
        # 计算当前小程序与截图尺寸的缩放比例
        scale_x = cr_window_pos["width"] / screenshot_width
        scale_y = cr_window_pos["height"] / screenshot_height
        print(f"  缩放比例: x={scale_x:.3f}, y={scale_y:.3f}")
        
        # 从按钮配置坐标反推按钮在截图中的相对位置
        button_config_x, button_config_y = button_pos
        screenshot_rel_x = (button_config_x - base_window_x) * 2
        screenshot_rel_y = (button_config_y - base_window_y) * 2
        print(f"  按钮在截图中的相对位置: ({screenshot_rel_x}, {screenshot_rel_y})")
        
        # 计算按钮在当前小程序窗口内的相对位置
        window_rel_x = screenshot_rel_x * scale_x
        window_rel_y = screenshot_rel_y * scale_y
        print(f"  按钮在当前窗口内的相对位置: ({window_rel_x:.1f}, {window_rel_y:.1f})")
        
        # 转换为当前屏幕的绝对坐标
        actual_x = cr_window_pos["x"] + window_rel_x
        actual_y = cr_window_pos["y"] + window_rel_y
        
        # 四舍五入到整数
        actual_x = int(actual_x)
        actual_y = int(actual_y)
        
        # 确保坐标在合理范围内，严格限制在皇室战争小程序窗口边界内
        actual_x = max(cr_window_pos["x"], min(actual_x, cr_window_pos["right"] - 1))
        actual_y = max(cr_window_pos["y"], min(actual_y, cr_window_pos["bottom"] - 1))
        
        print(f"  基准坐标: {button_pos} -> 转换为当前窗口坐标: ({actual_x}, {actual_y})")
        return actual_x, actual_y
    
    def action_battle_not_started(self):
        """战斗未开始状态的行为"""
        print("[智能行为] 战斗未开始 - 可以点击对战按钮开始战斗")
        # 模拟点击对战按钮
        if "对战按钮" in self.button_positions["战斗未开始"]:
            button_pos = self.button_positions["战斗未开始"]["对战按钮"]
            print(f"  按钮配置坐标: {button_pos} (百分比坐标)")
            # 直接使用ClickManager的click方法，它会自动处理百分比坐标转换
            return self.click_with_cliclick(button_pos[0], button_pos[1])  # 执行实际点击
        return False
    
    def action_battle_in_progress(self):
        """战斗中状态的行为"""
        print("[智能行为] 战斗进行中 - 可以发送表情或执行战斗操作")
        # 这里可以添加战斗中的智能操作
        # 例如：自动发送表情、使用卡牌等
        return True
    
    def action_battle_ended(self):
        """战斗结束状态的行为"""
        print("[智能行为] 战斗结束 - 点击确认按钮")
        # 模拟点击确认按钮
        if "确认按钮" in self.button_positions["战斗结束"]:
            button_pos = self.button_positions["战斗结束"]["确认按钮"]
            print(f"  按钮配置坐标: {button_pos} (百分比坐标)")
            # 直接使用ClickManager的click方法，它会自动处理百分比坐标转换
            return self.click_with_cliclick(button_pos[0], button_pos[1])  # 执行实际点击
        return False
    
    def action_opening_chest(self):
        """开宝箱状态的行为"""
        print("[智能行为] 开宝箱中 - 点击界面5次，每次间隔2秒")
        
        # 对于宝箱开启前状态，需要点击5次来预览奖励
        # 对于正式开宝箱状态，也需要点击多次来开启
        
        if "开宝箱按钮" in self.button_positions["开宝箱"]:
            button_pos = self.button_positions["开宝箱"]["开宝箱按钮"]
            print(f"  按钮配置坐标: {button_pos} (百分比坐标)")
            
            # 执行5次点击，每次间隔2秒
            for i in range(6):
                print(f"  第 {i+1}/5 次点击")
                self.click_with_cliclick(button_pos[0], button_pos[1])  # 直接使用百分比坐标
                # 最后一次点击后不需要等待
                if i < 4:
                    print("  等待2秒...")
                    time.sleep(2)
            
            return True
        return False