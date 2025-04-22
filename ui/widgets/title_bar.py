
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QMenu
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QPoint

class TitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("TitleBar")
        self.setFixedHeight(40)
        self.parent_window = parent

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)

        title = QLabel("🌟 StarLife Todo Manager")
        title.setStyleSheet("font-weight: bold;")
        layout.addWidget(title)
        layout.addStretch()

        btn_settings = QPushButton("⚙")
        btn_settings.setFixedWidth(30)
        btn_settings.clicked.connect(self.open_settings_menu)

        btn_min = QPushButton("—")
        btn_min.setFixedWidth(30)
        btn_min.clicked.connect(self.parent_window.showMinimized)

        btn_close = QPushButton("×")
        btn_close.setFixedWidth(30)
        btn_close.clicked.connect(self.parent_window.close)

        layout.addWidget(btn_settings)
        layout.addWidget(btn_min)
        layout.addWidget(btn_close)

        self.setMouseTracking(True)

    def open_settings_menu(self):
        menu = QMenu(self)
        lang = QAction("语言设置", self)
        style = QAction("样式设置", self)
        lang.triggered.connect(self.parent_window.open_language_dialog)
        style.triggered.connect(self.parent_window.open_style_dialog)
        menu.addAction(lang)
        menu.addAction(style)
        button = self.sender()
        menu.exec(button.mapToGlobal(button.rect().bottomLeft()))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and hasattr(self, "_drag_pos"):
            delta = event.globalPosition().toPoint() - self._drag_pos
            self.parent_window.move(self.parent_window.pos() + delta)
            self._drag_pos = event.globalPosition().toPoint()
