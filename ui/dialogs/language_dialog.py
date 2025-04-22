# ui/dialogs/language_dialog.py
from PySide6.QtWidgets import QDialog, QVBoxLayout, QComboBox, QPushButton, QLabel

class LanguageDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("选择语言")
        self.selected = "中文"
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("请选择语言："))

        self.combo = QComboBox()
        self.combo.addItems(["中文", "English", "日本語", "한국어"])
        layout.addWidget(self.combo)

        confirm_btn = QPushButton("确认")
        confirm_btn.clicked.connect(self.accept)
        layout.addWidget(confirm_btn)

        self.setLayout(layout)

    def selected_language(self):
        return self.combo.currentText()
