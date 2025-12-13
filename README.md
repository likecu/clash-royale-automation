# Clash Royale Screenshot Automation

This project automates screenshot capturing and processing for Clash Royale game.

## Features

- Automated screenshot capture
- Image file management
- Test scripts for image processing

## Project Structure

```
├── png/                 # Image resources organized by game states
│   ├── 战斗中/          # In-battle screenshots
│   ├── 战斗结束/        # Post-battle screenshots  
│   ├── 战斗未开始/      # Pre-battle screenshots
│   └── 开宝箱/          # Chest opening screenshots
├── screenshot.py        # Main screenshot automation script
├── test_image_files.py  # Test script for image file handling
└── .gitignore           # Git ignore configuration
```

## Usage

1. Ensure Python 3.8+ is installed
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the screenshot script:
   ```bash
   python screenshot.py
   ```
4. Run tests:
   ```bash
   python test_image_files.py
   ```

## Technologies Used

- Python 3
- Git
- Image processing libraries

## License

MIT
