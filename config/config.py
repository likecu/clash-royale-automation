# 皇室战争自动化工具配置文件

# 截图配置
SCREENSHOT_CONFIG = {
    "wechat_process_name": "WeChat",
    "weapp_relative_region": (0, 0, 400, 450),  # (相对x, 相对y, width, height)，相对于微信窗口左上角
    "screenshot_dir": "png",
    "prefix": "weapp_auto"
}

# 状态识别配置
STATUS_RECOGNITION_CONFIG = {
    "status_templates": {
        "战斗未开始": {
            "template_path": "png/战斗未开始/初始页面.png",
            "threshold": 0.8
        },
        "战斗中": {
            "template_path": "png/战斗中/对战界面.png",
            "threshold": 0.8
        },
        "战斗结束": {
            "template_path": "png/战斗结束/战斗结束页面.png",
            "threshold": 0.8
        },
        "开宝箱": {
            "template_path": "png/开宝箱/开宝箱界面.png",
            "threshold": 0.8
        }
    }
}

# 按钮位置配置
BUTTON_CONFIG = {
    "战斗未开始": {
        "对战按钮": (1205, 795)  # 计算得到的正确屏幕坐标
    },
    "战斗中": {
        "表情按钮": (1350, 850)  # 示例位置
    },
    "战斗结束": {
        "确认按钮": (1205, 882)  # 计算得到的正确屏幕坐标 (514*0.5+948=1205, 1701*0.5+31=882)
    },
    "开宝箱": {
        "开宝箱按钮": (1236, 928)  # 计算得到的正确屏幕坐标 (577*0.5+948=1236, 1793*0.5+31=928)
    }
}

# 按钮标记配置
BUTTON_MARK_CONFIG = {
    "png_dir": "png",
    "scenes": [
        "战斗未开始",
        "战斗中",
        "战斗结束", 
        "开宝箱"
    ],
    "scene_configs": {
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
}

# 豆包OCR配置
DOUBAO_OCR_CONFIG = {
    "ocr_script_path": "/Volumes/600g/app1/doubao获取/python/doubao_ocr.py",
    "node_script_path": "/Volumes/600g/app1/doubao获取/test_upload_image.js",
    "python_path": "/Volumes/600g/app1/okx-py/bin/python3"
}