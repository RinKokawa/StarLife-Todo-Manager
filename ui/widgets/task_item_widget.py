# ui/widgets/task_item_widget.py
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QGraphicsOpacityEffect
from PySide6.QtCore import Qt, QPropertyAnimation
from PySide6.QtCore import QEvent

class TaskItemWidget(QWidget):
    def __init__(self, task, edit_callback):
        super().__init__()
        self.task = task
        self.edit_callback = edit_callback
        self.init_ui()
        self.installEventFilter(self)  # 注册事件过滤器实现 hover 检测

    def init_ui(self):
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(5, 2, 5, 2)

        self.label = QLabel(str(self.task))
        self.label.setWordWrap(True)
        self.layout.addWidget(self.label)

        self.edit_button = QPushButton("编辑")
        self.edit_button.setFixedSize(60, 26)
        self.edit_button.clicked.connect(lambda: self.edit_callback(self.task))
        self.edit_button.setVisible(False)

        self.opacity = QGraphicsOpacityEffect(self.edit_button)
        self.edit_button.setGraphicsEffect(self.opacity)
        self.fade_anim = QPropertyAnimation(self.opacity, b"opacity")
        self.fade_anim.setDuration(200)

        self.layout.addWidget(self.edit_button)
        self.setLayout(self.layout)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Enter:
            self.show_edit_button()
        elif event.type() == QEvent.Leave:
            self.hide_edit_button()
        return super().eventFilter(obj, event)

    def show_edit_button(self):
        self.edit_button.setVisible(True)
        self.fade_anim.stop()
        self.fade_anim.setStartValue(0)
        self.fade_anim.setEndValue(1)
        self.fade_anim.start()

    def hide_edit_button(self):
        def hide_later():
            self.edit_button.setVisible(False)
            self.fade_anim.finished.disconnect(hide_later)  # ✅ 清理信号连接

        self.fade_anim.stop()
        self.fade_anim.setStartValue(1)
        self.fade_anim.setEndValue(0)
        self.fade_anim.finished.connect(hide_later)
        self.fade_anim.start()
