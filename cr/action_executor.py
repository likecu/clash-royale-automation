import pyautogui
from config.config import BUTTON_CONFIG

class ActionExecutor:
    """操作执行器，根据状态执行相应的操作"""
    
    def __init__(self):
        self.button_positions = BUTTON_CONFIG
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
    
    def action_battle_not_started(self):
        """战斗未开始状态的行为"""
        print("[智能行为] 战斗未开始 - 可以点击对战按钮开始战斗")
        # 模拟点击对战按钮
        if "对战按钮" in self.button_positions["战斗未开始"]:
            button_pos = self.button_positions["战斗未开始"]["对战按钮"]
            print(f"  点击位置: {button_pos}")
            # pyautogui.click(button_pos[0], button_pos[1])  # 取消注释以执行实际点击
            return True
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
            print(f"  点击位置: {button_pos}")
            # pyautogui.click(button_pos[0], button_pos[1])  # 取消注释以执行实际点击
            return True
        return False
    
    def action_opening_chest(self):
        """开宝箱状态的行为"""
        print("[智能行为] 开宝箱中 - 点击开宝箱按钮")
        # 模拟点击开宝箱按钮
        if "开宝箱按钮" in self.button_positions["开宝箱"]:
            button_pos = self.button_positions["开宝箱"]["开宝箱按钮"]
            print(f"  点击位置: {button_pos}")
            # pyautogui.click(button_pos[0], button_pos[1])  # 取消注释以执行实际点击
            return True
        return False