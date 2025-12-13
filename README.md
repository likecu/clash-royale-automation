# 皇室战争自动化游戏

这是一个用于皇室战争游戏的自动化项目，包含截图捕获、图片处理和自动化测试功能。

## 功能特性

- 自动截图捕获
- 图片文件管理
- 图像处理测试脚本

## 项目结构

```
├── png/                 # 按游戏状态分类的图片资源
│   ├── 战斗中/          # 战斗中的截图
│   ├── 战斗结束/        # 战斗结束后的截图  
│   ├── 战斗未开始/      # 战斗开始前的截图
│   └── 开宝箱/          # 开宝箱的截图
├── screenshot.py        # 主要的截图自动化脚本
├── test_image_files.py  # 图片文件处理测试脚本
└── .gitignore           # Git忽略配置
```

## 使用方法

1. 确保安装了Python 3.8+
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 运行截图脚本：
   ```bash
   python screenshot.py
   ```
4. 运行测试：
   ```bash
   python test_image_files.py
   ```

## 技术栈

- Python 3
- Git
- 图像处理库

## 许可证

MIT
