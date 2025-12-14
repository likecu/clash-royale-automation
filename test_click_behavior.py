#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试点击行为，记录皇室战争界面的点击位置并转换为百分比坐标
"""

import time
import subprocess
from cr import CRGameAutomation
from cr.click_manager import ClickManager

def record_click_positions():
    """记录皇室战争界面的点击位置并转换为百分比坐标"""
    print("皇室战争点击位置记录工具")
    print("=" * 50)
    
    # 创建点击管理器实例
    click_manager = ClickManager()
    
    # 更新皇室战争窗口区域
    click_manager.update_cr_window_region()
    
    # 获取皇室战争窗口信息
    cr_window = click_manager.get_cr_window_position()
    print(f"皇室战争窗口区域: ({cr_window['x']}, {cr_window['y']}, {cr_window['width']}, {cr_window['height']})")
    
    # 初始化点击位置列表
    click_positions = []
    
    print("\n=== 开始记录点击位置 ===")
    print("请在皇室战争界面上移动鼠标到想要记录的位置，然后按 Enter 键")
    print("按 Ctrl+C 停止记录")
    print("\n注意：每次按 Enter 后，会记录当前鼠标位置并显示百分比坐标")
    print("=" * 50)
    
    try:
        while True:
            # 提示用户移动鼠标并按Enter
            input("\n请移动鼠标到想要记录的位置，然后按 Enter 键...")
            
            # 使用cliclick获取当前鼠标位置
            # cliclick p 会打印当前鼠标位置，格式类似："123,456"
            result = subprocess.run(["cliclick", "p"], capture_output=True, text=True)
            
            # 解析输出结果
            output = result.stdout.strip()
            coords = output.split(",")
            if len(coords) == 2:
                try:
                    click_x = int(coords[0])
                    click_y = int(coords[1])
                    
                    # 检查点击位置是否在皇室战争窗口内
                    if click_manager.is_position_in_cr_window(click_x, click_y):
                        # 计算相对于皇室战争窗口的百分比坐标
                        rel_x = (click_x - cr_window['x']) / cr_window['width'] * 100
                        rel_y = (click_y - cr_window['y']) / cr_window['height'] * 100
                        
                        # 保存到列表
                        click_positions.append((rel_x, rel_y))
                        
                        # 打印结果
                        print(f"✓ 位置记录成功：")
                        print(f"  绝对坐标：({click_x}, {click_y})")
                        print(f"  百分比坐标：({rel_x:.2f}%, {rel_y:.2f}%)")
                        print(f"  坐标列表：{[(f'{x:.2f}%', f'{y:.2f}%') for x, y in click_positions]}")
                    else:
                        print(f"✗ 鼠标位置({click_x}, {click_y})不在皇室战争窗口内，已忽略")
                except ValueError:
                    print(f"✗ 无法解析鼠标位置：{output}")
            else:
                print(f"✗ 无法解析鼠标位置：{output}")
            
    except KeyboardInterrupt:
        print("\n" + "=" * 50)
        print("记录已停止")
        
    # 打印最终结果
    if click_positions:
        print("\n=== 最终记录结果 ===")
        print(f"共记录了 {len(click_positions)} 个位置：")
        for i, (x, y) in enumerate(click_positions, 1):
            print(f"  {i}. ({x:.2f}%, {y:.2f}%)")
        
        # 生成可直接使用的坐标列表
        coord_list_str = "[" + ", ".join([f"({x:.2f}, {y:.2f})" for x, y in click_positions]) + "]"
        print(f"\n可直接使用的坐标列表：")
        print(coord_list_str)
    else:
        print("\n没有记录到任何位置")
    
    print("\n" + "=" * 50)
    print("工具使用完成！")

def test_click_behavior():
    """测试点击行为，验证是否不再包含不必要的鼠标移动"""
    print("测试点击行为 - 验证是否不再包含不必要的鼠标移动")
    print("=" * 50)
    
    # 创建自动化工具实例
    cr_automation = CRGameAutomation()
    
    # 直接测试点击管理器的click方法
    print("\n测试click_manager的click方法:")
    from cr.click_manager import ClickManager
    click_manager = ClickManager()
    
    # 测试点击操作（不实际执行，只是验证代码流程）
    print("\n=== 模拟点击操作测试 ===")
    # 打印提示信息
    print("注意：这个测试会打印点击操作的执行流程，但不会实际执行点击")
    print("检查输出中是否不再包含 '移动鼠标' 的步骤")
    
    # 我们可以查看click方法的实现，确认不再包含鼠标移动
    import inspect
    click_method_source = inspect.getsource(click_manager.click)
    print("\nclick方法实现:")
    print(click_method_source)
    
    # 检查click方法中是否包含不必要的鼠标移动
    if "subprocess.run([\"cliclick\", f\"m:{\"" in click_method_source:
        print("\n✗ 错误：click方法中仍然包含不必要的鼠标移动操作")
    else:
        print("\n✓ 成功：click方法中不再包含不必要的鼠标移动操作")
    
    print("\n" + "=" * 50)
    print("测试完成！")

if __name__ == "__main__":
    # 运行点击位置记录功能
    record_click_positions()
    # 如需运行原有的点击行为测试，可取消下面的注释
    # test_click_behavior()
