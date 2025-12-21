from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image
import os

class YoloDetector:
    """YOLO检测器，用于检测皇室战争游戏画面中的元素和下兵位置"""
    
    def __init__(self, model_path='yolov8n.pt'):
        """初始化YOLO检测器
        
        参数:
            model_path: YOLO模型路径，默认使用预训练的yolov8n模型
        """
        # 加载YOLO模型
        self.model = YOLO(model_path)
        
        # 定义游戏相关的类别（根据实际训练情况调整）
        self.game_classes = {
            'troop': 0,        # 兵种
            'building': 1,     # 建筑
            'elixir': 2,       # 圣水
            'tower': 3,        # 防御塔
            'bridge': 4,       # 桥梁
            'barbarian_hut': 5,# 野蛮人小屋
            'king_tower': 6,   # 国王塔
            'princess_tower': 7# 公主塔
        }
        
        # 游戏区域参数（根据实际游戏画面调整）
        self.game_area = {
            'x1': 0,    # 游戏区域左上角x坐标
            'y1': 0,    # 游戏区域左上角y坐标
            'x2': 1000, # 游戏区域右下角x坐标
            'y2': 600   # 游戏区域右下角y坐标
        }
    
    def detect_game_elements(self, image_path):
        """检测游戏画面中的元素
        
        参数:
            image_path: 游戏截图路径
            
        返回:
            results: 检测结果，包含各类元素的位置和置信度
        """
        if not os.path.exists(image_path):
            print(f"✗ 图片不存在: {image_path}")
            return None
        
        # 加载图片
        image = cv2.imread(image_path)
        if image is None:
            print(f"✗ 无法加载图片: {image_path}")
            return None
        
        # 使用YOLO模型进行检测
        results = self.model(image)
        
        # 处理检测结果
        detected_elements = {
            'troops': [],
            'buildings': [],
            'towers': [],
            'elixir': None,
            'bridges': []
        }
        
        # 遍历检测结果
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # 获取类别ID和置信度
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                
                # 只保留置信度大于0.5的检测结果
                if confidence < 0.5:
                    continue
                
                # 获取边界框坐标
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                # 计算中心点坐标
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2
                
                # 根据类别分类
                element = {
                    'class_id': class_id,
                    'confidence': confidence,
                    'bbox': [x1, y1, x2, y2],
                    'center': [center_x, center_y]
                }
                
                # 根据类别添加到相应列表
                if class_id == self.game_classes['troop']:
                    detected_elements['troops'].append(element)
                elif class_id == self.game_classes['building']:
                    detected_elements['buildings'].append(element)
                elif class_id in [self.game_classes['tower'], self.game_classes['king_tower'], self.game_classes['princess_tower']]:
                    detected_elements['towers'].append(element)
                elif class_id == self.game_classes['bridge']:
                    detected_elements['bridges'].append(element)
        
        return detected_elements
    
    def calculate_best_deploy_position(self, detected_elements, image_shape):
        """计算最佳下兵位置
        
        参数:
            detected_elements: 检测到的游戏元素
            image_shape: 图片形状 (高度, 宽度, 通道数)
            
        返回:
            best_position: 最佳下兵位置 (x, y)
        """
        if not detected_elements:
            return None
        
        height, width = image_shape[:2]
        
        # 精确划分游戏区域（根据皇室战争实际游戏布局）
        game_regions = {
            'my_area': {
                'x1': 0,              # 我方区域左侧
                'x2': width // 2,     # 我方区域右侧（中线）
                'y1': height // 4,    # 我方区域上方
                'y2': height * 3 // 4 # 我方区域下方
            },
            'enemy_area': {
                'x1': width // 2,     # 敌方区域左侧（中线）
                'x2': width,          # 敌方区域右侧
                'y1': height // 4,    # 敌方区域上方
                'y2': height * 3 // 4 # 敌方区域下方
            },
            'bridge_area': {
                'x1': width * 2 // 5,  # 桥梁区域左侧
                'x2': width * 3 // 5,  # 桥梁区域右侧
                'y1': height // 3,     # 桥梁区域上方
                'y2': height * 2 // 3  # 桥梁区域下方
            },
            'my_defense_area': {
                'x1': 0,              # 我方防御区域左侧
                'x2': width // 4,     # 我方防御区域右侧
                'y1': height // 3,     # 我方防御区域上方
                'y2': height * 2 // 3  # 我方防御区域下方
            },
            'my_attack_area': {
                'x1': width // 4,      # 我方攻击区域左侧
                'x2': width // 2,     # 我方攻击区域右侧
                'y1': height // 3,     # 我方攻击区域上方
                'y2': height * 2 // 3  # 我方攻击区域下方
            }
        }
        
        # 基础推荐位置列表（根据游戏策略）
        base_positions = [
            (width // 3, height // 3),      # 左上攻击位置
            (width // 3, height // 2),      # 中间攻击位置
            (width // 3, height * 2 // 3),  # 左下攻击位置
            (width // 4, height // 2),      # 防御位置
            (width * 3 // 10, height // 2)  # 推进位置
        ]
        
        # 初始化最佳位置
        best_position = base_positions[1]  # 默认使用中间攻击位置
        
        # 1. 检查是否有敌方单位，选择在敌方单位前进路线前方
        if detected_elements['troops'] or detected_elements['buildings']:
            # 找到最靠近我方的敌方单位
            closest_enemy = None
            closest_distance = float('inf')
            
            # 我方区域中心
            my_center = [width // 4, height // 2]
            
            # 检查所有敌方单位
            all_enemies = detected_elements['troops'] + detected_elements['buildings']
            for enemy in all_enemies:
                # 计算敌方单位到我方中心的距离
                distance = np.sqrt(
                    (enemy['center'][0] - my_center[0]) ** 2 +
                    (enemy['center'][1] - my_center[1]) ** 2
                )
                
                if distance < closest_distance:
                    closest_distance = distance
                    closest_enemy = enemy
            
            if closest_enemy:
                # 计算敌方单位相对于我方的位置
                enemy_x, enemy_y = closest_enemy['center']
                
                # 根据敌方位置选择合适的下兵位置
                if enemy_y < height // 3:
                    # 敌方在上半部分，选择上方攻击位置
                    best_position = base_positions[0]
                elif enemy_y > height * 2 // 3:
                    # 敌方在下半部分，选择下方攻击位置
                    best_position = base_positions[2]
                else:
                    # 敌方在中间，选择中间攻击位置
                    best_position = base_positions[1]
        
        # 2. 检查是否有桥梁，优先考虑桥梁附近
        elif detected_elements['bridges']:
            # 选择桥梁区域的中心位置
            bridge = detected_elements['bridges'][0]
            bridge_x, bridge_y = bridge['center']
            
            # 桥梁附近的攻击位置
            best_position = (int(bridge_x - width // 10), bridge_y)
        
        # 3. 如果没有检测到特殊元素，根据图片尺寸动态调整
        else:
            # 生成随机偏移，增加位置多样性
            import random
            offset_x = random.randint(-50, 50)
            offset_y = random.randint(-50, 50)
            
            # 从基础位置中随机选择一个
            import random
            selected_base = random.choice(base_positions)
            best_position = (
                selected_base[0] + offset_x,
                selected_base[1] + offset_y
            )
        
        # 4. 确保位置在有效范围内
        best_x = max(game_regions['my_area']['x1'], min(best_position[0], game_regions['my_area']['x2']))
        best_y = max(game_regions['my_area']['y1'], min(best_position[1], game_regions['my_area']['y2']))
        
        best_position = (int(best_x), int(best_y))
        
        return best_position
    
    def visualize_detection(self, image_path, detected_elements, deploy_position=None):
        """可视化检测结果
        
        参数:
            image_path: 原始图片路径
            detected_elements: 检测到的游戏元素
            deploy_position: 建议的下兵位置
            
        返回:
            visualized_image: 可视化后的图片
        """
        if not os.path.exists(image_path):
            print(f"✗ 图片不存在: {image_path}")
            return None
        
        # 加载图片
        image = cv2.imread(image_path)
        if image is None:
            print(f"✗ 无法加载图片: {image_path}")
            return None
        
        # 绘制检测到的元素
        colors = {
            'troops': (0, 255, 0),      # 绿色 - 兵种
            'buildings': (0, 0, 255),    # 红色 - 建筑
            'towers': (255, 0, 0),       # 蓝色 - 防御塔
            'bridges': (255, 255, 0)     # 黄色 - 桥梁
        }
        
        # 绘制兵种
        for troop in detected_elements['troops']:
            x1, y1, x2, y2 = troop['bbox']
            cv2.rectangle(image, (x1, y1), (x2, y2), colors['troops'], 2)
            cv2.putText(image, f"Troop: {troop['confidence']:.2f}", 
                       (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors['troops'], 2)
        
        # 绘制建筑
        for building in detected_elements['buildings']:
            x1, y1, x2, y2 = building['bbox']
            cv2.rectangle(image, (x1, y1), (x2, y2), colors['buildings'], 2)
            cv2.putText(image, f"Building: {building['confidence']:.2f}", 
                       (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors['buildings'], 2)
        
        # 绘制防御塔
        for tower in detected_elements['towers']:
            x1, y1, x2, y2 = tower['bbox']
            cv2.rectangle(image, (x1, y1), (x2, y2), colors['towers'], 2)
            cv2.putText(image, f"Tower: {tower['confidence']:.2f}", 
                       (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors['towers'], 2)
        
        # 绘制桥梁
        for bridge in detected_elements['bridges']:
            x1, y1, x2, y2 = bridge['bbox']
            cv2.rectangle(image, (x1, y1), (x2, y2), colors['bridges'], 2)
            cv2.putText(image, f"Bridge: {bridge['confidence']:.2f}", 
                       (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colors['bridges'], 2)
        
        # 绘制最佳下兵位置
        if deploy_position:
            x, y = deploy_position
            # 绘制大的绿色圆圈表示下兵位置
            cv2.circle(image, (x, y), 20, (0, 255, 0), -1)
            cv2.circle(image, (x, y), 25, (0, 255, 0), 3)
            cv2.putText(image, "最佳下兵位置", 
                       (x - 60, y - 35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        return image
    
    def save_visualization(self, image, output_path):
        """保存可视化结果
        
        参数:
            image: 可视化后的图片
            output_path: 输出路径
        """
        cv2.imwrite(output_path, image)
        print(f"✓ 可视化结果已保存: {output_path}")
    
    def detect_and_visualize(self, image_path, output_path=None):
        """检测游戏画面并可视化结果
        
        参数:
            image_path: 游戏截图路径
            output_path: 可视化结果输出路径，默认在原路径后添加_detection
            
        返回:
            best_position: 最佳下兵位置
        """
        # 检测游戏元素
        detected_elements = self.detect_game_elements(image_path)
        if not detected_elements:
            return None
        
        # 获取图片形状
        image = cv2.imread(image_path)
        image_shape = image.shape
        
        # 计算最佳下兵位置
        best_position = self.calculate_best_deploy_position(detected_elements, image_shape)
        
        # 可视化结果
        visualized_image = self.visualize_detection(image_path, detected_elements, best_position)
        
        # 保存可视化结果
        if not output_path:
            output_path = image_path.replace('.png', '_detection.png')
        self.save_visualization(visualized_image, output_path)
        
        return best_position
