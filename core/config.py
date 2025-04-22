
import json
import os
from pathlib import Path
from PySide6.QtWidgets import QApplication

DATA_PATH = Path.home() / ".stodolist"
CONFIG_FILE = DATA_PATH / "config.json"

def apply_stylesheet(app: QApplication):
    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                qss_filename = data.get("style", "candy.qss")
                qss_path = os.path.join(os.path.dirname(__file__), "../assets/qss", qss_filename)
                if os.path.exists(qss_path):
                    with open(qss_path, "r", encoding="utf-8") as qss_file:
                        app.setStyleSheet(qss_file.read())
    except Exception as e:
        print("样式加载失败:", e)

def init_config():
    if not DATA_PATH.exists():
        DATA_PATH.mkdir()
    if not CONFIG_FILE.exists():
        default = {
            "statuses": ["pending", "done"],
            "language": "中文",
            "style": "candy.qss"
        }
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(default, f, indent=2, ensure_ascii=False)

def load_statuses():
    default_statuses = ["pending", "done"]
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("statuses", default_statuses)
        except Exception:
            return default_statuses
    else:
        return default_statuses

def set_language(lang):
    try:
        config = {}
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
        config["language"] = lang
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print("语言设置失败:", e)

def set_style(style_filename):
    try:
        config = {}
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
        config["style"] = style_filename
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print("样式设置失败:", e)

def get_language():
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("language", "中文")
        except Exception:
            return "中文"
    return "中文"
