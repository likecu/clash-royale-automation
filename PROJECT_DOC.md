# 皇室战争自动化工具 - 项目文档

## 1. 项目概述

皇室战争自动化工具是一个基于Python开发的游戏辅助工具，专注于皇室战争微信小程序的自动化操作。该工具整合了屏幕截图、状态识别、按钮标记和智能操作执行等功能，旨在提高游戏体验和自动化程度。

## 2. 项目结构

项目采用模块化设计，将不同功能拆分为独立模块，便于维护和扩展。

```
皇室战争/
├── cr/                 # 核心功能模块
│   ├── __init__.py     # 包初始化文件
│   ├── automation.py   # 自动化核心类，整合所有模块
│   ├── screenshot.py   # 截图功能模块
│   ├── status_recognizer.py  # 状态识别模块
│   ├── button_marker.py       # 按钮标记模块
│   ├── action_executor.py     # 操作执行模块
│   ├── click_manager.py       # 点击操作管理模块
│   └── utils.py               # 公共工具模块
├── config/             # 配置文件目录
│   └── config.py       # 集中配置管理
├── png/                # 图片资源目录
│   ├── 战斗未开始/     # 战斗未开始状态图片
│   ├── 战斗中/         # 战斗中状态图片
│   ├── 战斗结束/       # 战斗结束状态图片
│   ├── 开宝箱/         # 开宝箱状态图片
│   └── 实际游戏截图/    # 实际游戏截图，按状态分类
│       ├── 战斗中/     # 实际战斗中截图
│       ├── 战斗未开始/ # 实际战斗未开始截图
│       ├── 战斗结束/   # 实际战斗结束截图
│       └── 其他/       # 其他实际游戏截图
├── test/               # 测试用例目录
│   ├── test_automation.py      # 自动化测试
│   ├── test_screenshot_performance.py  # 截图性能测试
│   ├── test_status_recognition.py     # 状态识别测试
│   └── test_utils.py                 # 工具函数测试
├── main.py             # 主入口文件
├── extract_elixir.py   # 圣水数量提取脚本
├── README.md           # 项目说明文档
└── PROJECT_DOC.md      # 项目详细文档
```

## 3. 核心功能

### 3.1 自动截图功能

**功能描述**：自动截取微信小程序中的皇室战争界面，支持单张截图和批量截图。

**实现方式**：
- 使用Mac系统的`screencapture`命令进行截图
- 支持按指定区域截图，可配置截图区域
- 支持批量截图，可设置截图次数和间隔时间
- 截图文件自动添加时间戳，便于管理

**使用方法**：
```python
from cr import CRGameAutomation

# 创建自动化工具实例
cr_automation = CRGameAutomation()

# 实时截图并分析
status, screenshot_path = cr_automation.capture_and_analyze()

# 批量截图
cr_automation.screenshot_manager.batch_screenshot_weapp(count=3, interval=5, prefix="weapp_batch")
```

### 3.2 状态识别功能

**功能描述**：识别当前游戏截图所属的状态，支持4种游戏状态：战斗未开始、战斗中、战斗结束、开宝箱。

**实现方式**：
- 使用模板匹配算法进行状态识别
- 结合页面相似度和按钮相似度进行综合判断
- 为不同状态设置不同的匹配权重和阈值
- 支持自定义状态模板和阈值

**使用方法**：
```python
# 分析现有截图
status, similarity = cr_automation.analyze_existing_screenshot("png/战斗未开始/初始页面.png")

# 批量分析截图
results = cr_automation.batch_analyze_screenshots("png")
```

### 3.3 按钮标记功能

**功能描述**：在截图上自动标记按钮位置，便于查看和验证。

**实现方式**：
- 支持按状态标记不同按钮
- 支持批量标记所有场景的按钮
- 标记后自动保存新的截图文件
- 可验证标记结果

**使用方法**：
```python
# 标记指定截图的按钮
marked_path = cr_automation.mark_button_on_screenshot("png/战斗未开始/初始页面.png", "战斗未开始")

# 标记所有场景的按钮
marked_files = cr_automation.mark_all_buttons()

# 验证标记结果
cr_automation.verify_marked_buttons(marked_files)
```

### 3.4 智能操作执行

**功能描述**：根据识别到的状态执行相应的操作，支持自定义操作映射。

**实现方式**：
- 为不同状态配置不同的操作
- 支持点击、双击、鼠标移动等操作
- 使用百分比坐标，适配不同屏幕分辨率
- 操作前进行边界检查，确保操作安全

**使用方法**：
```python
# 截取屏幕并执行智能操作
status, screenshot_path = cr_automation.capture_and_analyze(execute_action=True)

# 直接执行智能操作
cr_automation.execute_smart_action(status, screenshot_path)
```

### 3.5 圣水数量提取

**功能描述**：从战斗截图中提取圣水数量，支持单张图片和批量处理。

**实现方式**：
- 调用豆包OCR工具识别截图中的圣水数量
- 使用正则表达式提取纯净的圣水数量
- 将识别结果保存到JSON文件

**使用方法**：
```bash
# 处理单张图片
/Volumes/600g/app1/okx-py/bin/python3 extract_elixir.py png/实际游戏截图/战斗中/战斗中.png

# 批量处理战斗截图
/Volumes/600g/app1/okx-py/bin/python3 extract_elixir.py
```

## 4. 配置说明

所有配置集中在 `config/config.py` 文件中，主要配置项包括：

### 4.1 截图配置

```python
SCREENSHOT_CONFIG = {
    "wechat_process_name": "WeChat",  # 微信进程名称
    "weapp_relative_region": (0, 0, 335, 640),  # 相对截图区域 (x, y, width, height)
    "screenshot_dir": "png",  # 截图保存目录
    "prefix": "weapp_auto"  # 截图文件名前缀
}
```

### 4.2 状态识别配置

```python
STATUS_RECOGNITION_CONFIG = {
    "status_templates": {
        "战斗未开始": {
            "template_path": "png/战斗未开始/初始页面.png",
            "threshold": 0.70  # 匹配阈值
        },
        # 其他状态配置...
    }
}
```

### 4.3 按钮位置配置

```python
BUTTON_CONFIG = {
    "战斗未开始": {
        "对战按钮": (53.43, 80.78)  # 相对于皇室战争界面的百分比 (x%, y%)
    },
    # 其他状态按钮配置...
}
```

## 5. 安装和依赖

### 5.1 依赖库

- Pillow: 图片处理
- numpy: 数值计算
- cliclick: 屏幕点击操作（Mac系统原生工具）

### 5.2 安装方法

使用虚拟环境Python安装依赖：

```bash
/Volumes/600g/app1/okx-py/bin/python3 -m pip install pillow numpy
```

### 5.3 系统工具依赖

- cliclick: Mac系统下的命令行点击工具，用于执行鼠标操作
  - 安装方法：`brew install cliclick`

## 6. 使用方法

### 6.1 基本使用

运行主程序查看演示：

```bash
/Volumes/600g/app1/okx-py/bin/python3 main.py
```

### 6.2 在Python代码中使用

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

## 7. 扩展开发

### 7.1 添加新的状态

1. 在 `png` 目录下添加新状态的模板图片
2. 在 `config/config.py` 的 `STATUS_RECOGNITION_CONFIG` 中添加新状态配置
3. 在 `action_executor.py` 中添加对应的操作方法
4. 在 `action_map` 中添加状态到操作的映射

### 7.2 调整截图区域

修改 `config/config.py` 中的 `weapp_region` 配置项，根据实际屏幕分辨率调整截图区域。

## 8. 注意事项

1. 确保微信应用已经启动并登录
2. 调整截图区域时，需要根据实际屏幕分辨率进行设置
3. 模板图片需要与实际游戏界面保持一致
4. 按钮位置坐标需要根据实际屏幕分辨率调整
5. 使用豆包验证功能时，确保已配置正确的OCR工具路径

## 9. 项目优势

1. 模块化设计，便于维护和扩展
2. 支持多种游戏状态识别
3. 智能操作执行，提高自动化程度
4. 灵活的配置选项，适配不同场景
5. 完善的测试用例，确保功能稳定
6. 详细的文档，便于使用和开发

## 10. 未来展望

1. 支持更多游戏状态和操作
2. 优化状态识别算法，提高识别准确率
3. 添加机器学习模型，实现更智能的状态识别
4. 支持更多平台和设备
5. 增强用户界面，提供可视化配置选项
6. 添加更多游戏辅助功能

## 11. 联系方式

如有问题或建议，请通过GitHub Issue反馈。

---

**文档版本**：v1.0
**更新日期**：2025-12-17
**作者**：皇室战争自动化工具开发团队