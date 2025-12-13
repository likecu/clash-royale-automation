# 皇室战争自动化工具

一个基于Python的皇室战争游戏自动化工具，支持屏幕截图、状态识别、按钮标记和智能操作执行。

## 项目架构

项目采用模块化设计，将不同功能拆分为独立模块，便于维护和扩展。

```
皇室战争/
├── cr/                 # 核心功能模块
│   ├── __init__.py     # 包初始化文件
│   ├── automation.py   # 自动化核心类，整合所有模块
│   ├── screenshot.py   # 截图功能模块
│   ├── status_recognizer.py  # 状态识别模块
│   ├── button_marker.py       # 按钮标记模块
│   └── action_executor.py     # 操作执行模块
├── config/             # 配置文件目录
│   └── config.py       # 集中配置管理
├── png/                # 图片资源目录
│   ├── 战斗未开始/     # 战斗未开始状态图片
│   ├── 战斗中/         # 战斗中状态图片
│   ├── 战斗结束/       # 战斗结束状态图片
│   └── 开宝箱/         # 开宝箱状态图片
├── main.py             # 主入口文件
├── .gitignore          # Git忽略文件
└── README.md           # 项目说明文档
```

## 模块说明

### 1. 自动化核心 (automation.py)
- 整合所有功能模块
- 提供统一的API接口
- 支持截图、分析、操作执行一体化流程

### 2. 截图模块 (screenshot.py)
- 自动截取WeApp界面
- 支持批量截图
- 可配置截图区域和文件名格式

### 3. 状态识别模块 (status_recognizer.py)
- 支持4种游戏状态识别：战斗未开始、战斗中、战斗结束、开宝箱
- 使用模板匹配算法
- 可配置相似度阈值

### 4. 按钮标记模块 (button_marker.py)
- 在截图上自动标记按钮位置
- 支持模板匹配查找按钮
- 可使用豆包验证标记结果

### 5. 操作执行模块 (action_executor.py)
- 根据识别到的状态执行相应操作
- 支持自定义操作映射
- 可扩展添加更多操作

## 配置说明

所有配置集中在 `config/config.py` 文件中，主要配置项包括：

### 截图配置
```python
SCREENSHOT_CONFIG = {
    "wechat_process_name": "WeChat",  # 微信进程名称
    "weapp_region": (948, 31, 513, 955),  # 截图区域 (x, y, width, height)
    "screenshot_dir": "png",  # 截图保存目录
    "prefix": "weapp_auto"  # 截图文件名前缀
}
```

### 状态识别配置
```python
STATUS_RECOGNITION_CONFIG = {
    "status_templates": {
        "战斗未开始": {
            "template_path": "png/战斗未开始/初始页面.png",
            "threshold": 0.8  # 匹配阈值
        },
        # 其他状态配置...
    }
}
```

### 按钮位置配置
```python
BUTTON_CONFIG = {
    "战斗未开始": {
        "对战按钮": (1200, 850)  # 按钮坐标位置
    },
    # 其他状态按钮配置...
}
```

## 安装和依赖

### 依赖库
- Pillow: 图片处理
- numpy: 数值计算
- cliclick: 屏幕点击操作（Mac系统原生工具）

### 安装方法
使用虚拟环境Python安装依赖：
```bash
/Volumes/600g/app1/okx-py/bin/python3 -m pip install pillow numpy
```

### 系统工具依赖
- cliclick: Mac系统下的命令行点击工具，用于执行鼠标操作
  - 安装方法：`brew install cliclick`

## 使用方法

### 基本使用

1. 运行主程序查看演示：
```bash
/Volumes/600g/app1/okx-py/bin/python3 main.py
```

2. 在Python代码中使用：
```python
from cr import CRGameAutomation

# 创建自动化工具实例
cr_automation = CRGameAutomation()

# 实时截图并分析
status, screenshot_path = cr_automation.capture_and_analyze()

# 分析现有截图
cr_automation.analyze_existing_screenshot("png/战斗未开始/初始页面.png")

# 批量分析截图
cr_automation.batch_analyze_screenshots("png")

# 标记按钮
cr_automation.mark_button_on_screenshot("png/战斗未开始/初始页面.png", "战斗未开始")

# 标记所有场景按钮
marked_files = cr_automation.mark_all_buttons()

# 验证标记结果
cr_automation.verify_marked_buttons(marked_files)
```

### 功能示例

#### 1. 实时截图和智能分析
```python
from cr import CRGameAutomation

cr_automation = CRGameAutomation()
# 截取屏幕并分析状态，执行相应操作
status, screenshot_path = cr_automation.capture_and_analyze()
```

#### 2. 批量分析现有截图
```python
from cr import CRGameAutomation

cr_automation = CRGameAutomation()
# 分析png目录下所有截图
results = cr_automation.batch_analyze_screenshots("png")
```

#### 3. 标记按钮位置
```python
from cr import CRGameAutomation

cr_automation = CRGameAutomation()
# 在截图上标记按钮
marked_path = cr_automation.mark_button_on_screenshot("png/战斗未开始/初始页面.png", "战斗未开始")
```

## 扩展开发

### 添加新的状态

1. 在 `png` 目录下添加新状态的模板图片
2. 在 `config/config.py` 的 `STATUS_RECOGNITION_CONFIG` 中添加新状态配置
3. 在 `action_executor.py` 中添加对应的操作方法
4. 在 `action_map` 中添加状态到操作的映射

### 调整截图区域

修改 `config/config.py` 中的 `weapp_region` 配置项，根据实际屏幕分辨率调整截图区域。

## 注意事项

1. 确保微信应用已经启动并登录
2. 调整截图区域时，需要根据实际屏幕分辨率进行设置
3. 模板图片需要与实际游戏界面保持一致
4. 按钮位置坐标需要根据实际屏幕分辨率调整
5. 使用豆包验证功能时，确保已配置正确的OCR工具路径

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 联系方式

如有问题或建议，请通过GitHub Issue反馈。
