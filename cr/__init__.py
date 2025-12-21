# 皇室战争自动化工具包

from cr.automation import CRGameAutomation
from cr.screenshot import ScreenshotManager
from cr.status_recognizer import StatusRecognizer
from cr.button_marker import ButtonMarker
from cr.action_executor import ActionExecutor
from cr.yolo_detector import YoloDetector

__all__ = [
    'CRGameAutomation',
    'ScreenshotManager',
    'StatusRecognizer',
    'ButtonMarker',
    'ActionExecutor',
    'YoloDetector'
]
