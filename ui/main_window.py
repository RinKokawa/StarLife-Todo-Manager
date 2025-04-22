
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PySide6.QtCore import Qt, QPoint
from ui.widgets.title_bar import TitleBar
from ui.widgets.task_panel import TaskPanel
from ui.mixins.resize_mixin import ResizeMixin
from core.config import load_statuses
from core.storage import load_tasks, save_tasks
from ui.dialogs.edit_task_dialog import EditTaskDialog
from ui.dialogs.language_dialog import LanguageDialog
from ui.dialogs.style_settings_dialog import StyleSettingsDialog

class MainWindow(QMainWindow, ResizeMixin):
    def __init__(self):
        super().__init__()
        ResizeMixin.__init__(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMouseTracking(True)
        self.setWindowTitle("StarLife Todo Manager")

        self.statuses = load_statuses()
        self.tasks = []

        self.init_ui()
        self.load()

    def init_ui(self):
        central_widget = QWidget()
        central_widget.setMouseTracking(True)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        self.title_bar = TitleBar(self)
        self.task_panel = TaskPanel(self, self.statuses)

        layout.addWidget(self.title_bar)
        layout.addWidget(self.task_panel)

        self.title_bar.setMouseTracking(True)
        self.task_panel.setMouseTracking(True)

    def load(self):
        self.tasks = load_tasks()
        self.task_panel.set_tasks(self.tasks)

    def edit_task(self, task):
        def on_save(updated_task):
            save_tasks(self.tasks)
            self.task_panel.refresh_list()
        dialog = EditTaskDialog(task, on_save)
        dialog.exec()

    def open_language_dialog(self):
        dialog = LanguageDialog()
        if dialog.exec():
            from core.config import set_language
            lang = dialog.selected_language()
            set_language(lang)

    def open_style_dialog(self):
        dlg = StyleSettingsDialog(self)
        dlg.exec()

    def mouseMoveEvent(self, event):
        if self._resizing:
            self._resize_window(event.globalPosition().toPoint())
        else:
            direction = self._get_resize_direction(event.pos())
            if direction:
                cursors = {
                    "left": Qt.SizeHorCursor,
                    "right": Qt.SizeHorCursor,
                    "top": Qt.SizeVerCursor,
                    "bottom": Qt.SizeVerCursor,
                    "top_left": Qt.SizeFDiagCursor,
                    "top_right": Qt.SizeBDiagCursor,
                    "bottom_left": Qt.SizeBDiagCursor,
                    "bottom_right": Qt.SizeFDiagCursor,
                }
                self.setCursor(cursors[direction])
            else:
                self.setCursor(Qt.ArrowCursor)

    def mousePressEvent(self, event):
        ResizeMixin.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        ResizeMixin.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
        ResizeMixin.mouseReleaseEvent(self, event)