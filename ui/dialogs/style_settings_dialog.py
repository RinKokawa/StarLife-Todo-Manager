# ui/dialogs/style_settings_dialog.py
import subprocess
import os
import sys
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox

class StyleSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("选择样式")
        self.resize(300, 150)
        self.qss_dir = os.path.join(os.path.dirname(__file__), "../../assets/qss")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("选择一个主题样式："))

        self.combo = QComboBox()
        self.combo.addItems(self.available_styles())
        layout.addWidget(self.combo)

        apply_btn = QPushButton("应用")
        apply_btn.clicked.connect(self.apply_selected_style)
        layout.addWidget(apply_btn)

        self.setLayout(layout)

    def available_styles(self):
        if not os.path.exists(self.qss_dir):
            return []
        return [f for f in os.listdir(self.qss_dir) if f.endswith(".qss")]


    def apply_selected_style(self):
        selected = self.combo.currentText()
        config_path = os.path.join(os.path.dirname(__file__), "../../config.txt")
        try:
            with open(config_path, "w", encoding="utf-8") as f:
                f.write(selected)

            QMessageBox.information(self, "成功", f"已应用样式：{selected}，即将重启程序。")
            
            # ✅ 启动一个新进程再退出
            subprocess.Popen([sys.executable] + sys.argv)
            sys.exit()

        except Exception as e:
            QMessageBox.critical(self, "失败", f"写入配置失败：{e}")
