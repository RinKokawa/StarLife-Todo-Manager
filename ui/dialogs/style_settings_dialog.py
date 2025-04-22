
# import sys
import sys, subprocess
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QListWidget, QPushButton, QMessageBox
from PySide6.QtCore import QCoreApplication
import os
from core.config import set_style

class StyleSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("样式设置")
        self.resize(400, 300)

        layout = QVBoxLayout(self)

        label = QLabel("选择样式：")
        layout.addWidget(label)

        self.qss_list = QListWidget()
        qss_dir = os.path.join(os.path.dirname(__file__), "../../assets/qss")
        for file in os.listdir(qss_dir):
            if file.endswith(".qss"):
                self.qss_list.addItem(file)
        layout.addWidget(self.qss_list)

        apply_button = QPushButton("应用样式并重启")
        apply_button.clicked.connect(self.apply_selected_style)
        layout.addWidget(apply_button)

    def apply_selected_style(self):
        selected_item = self.qss_list.currentItem()
        if selected_item:
            filename = selected_item.text()
            set_style(filename)
            QMessageBox.information(self, "提示", "样式已更换，正在重启应用...")
            python = sys.executable
            script = sys.argv[0]
            subprocess.Popen([python, script])
            QCoreApplication.quit()