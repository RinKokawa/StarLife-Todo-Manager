
import os
from tkinter import Menu
from PySide6.QtWidgets import QMenu

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QListWidget, QListWidgetItem,
    QMessageBox, QDateTimeEdit, QComboBox, QLabel, QFileDialog
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QDateTime, QSize, QPoint
from core.model import Task
from core.storage import load_tasks, save_tasks
from core.config import load_statuses, set_language
from ui.widgets.task_item_widget import TaskItemWidget
from ui.dialogs.edit_task_dialog import EditTaskDialog
from ui.dialogs.language_dialog import LanguageDialog
from ui.dialogs.style_settings_dialog import StyleSettingsDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("生活TodoList - StarLife Alpha")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.tasks = []
        self.statuses = load_statuses()
        self.current_filter = "all"
        self._resize_margin = 5
        self._resizing = False
        self._resize_direction = None
        self.init_ui()
        self.load()

    def init_ui(self):
        # self._init_menu()  # 菜单栏已被隐藏
        central_widget = QWidget()
        full_layout = QVBoxLayout()
        full_layout.setContentsMargins(0, 0, 0, 0)
        full_layout.setSpacing(0)

        full_layout.addWidget(self._create_title_bar())
        full_layout.addLayout(self._create_main_layout())

        central_widget.setLayout(full_layout)
        self.setCentralWidget(central_widget)
        self.menu_list.setCurrentRow(0)
        self.apply_stylesheet("assets/style.qss")

    def _create_title_bar(self):
        bar = QWidget()
        bar.setObjectName("TitleBar")
        bar.setFixedHeight(40)
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(10, 0, 10, 0)

        title = QLabel("🌟 StarLife Todo Manager")
        title.setStyleSheet("font-weight: bold;")

        layout.addWidget(title)
        layout.addStretch()

        # 新增：设置按钮
        btn_settings = QPushButton("⚙")
        btn_settings.setFixedWidth(30)
        btn_settings.clicked.connect(self.open_settings_menu)

        btn_min = QPushButton("—")
        btn_min.setFixedWidth(30)
        btn_min.clicked.connect(self.showMinimized)

        btn_close = QPushButton("×")
        btn_close.setFixedWidth(30)
        btn_close.clicked.connect(self.close)

        layout.addWidget(btn_settings)
        layout.addWidget(btn_min)
        layout.addWidget(btn_close)

        bar.mousePressEvent = self.mousePressEvent
        bar.mouseMoveEvent = self.mouseMoveEvent

        return bar

    def _create_main_layout(self):
        main_layout = QHBoxLayout()

        self.menu_list = QListWidget()
        self.menu_list.addItem("📋 所有任务")
        self.menu_list.addItem("⏳ 未完成任务")
        self.menu_list.addItem("✅ 已完成任务")
        self.menu_list.setFixedWidth(120)
        self.menu_list.currentRowChanged.connect(self.change_filter)
        main_layout.addWidget(self.menu_list)

        right_layout = QVBoxLayout()
        self.task_list = QListWidget()
        right_layout.addWidget(self.task_list)

        form_layout = QHBoxLayout()
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("任务标题")
        self.tag_input = QLineEdit()
        self.tag_input.setPlaceholderText("标签")
        self.deadline_input = QDateTimeEdit()
        self.deadline_input.setCalendarPopup(True)
        self.deadline_input.setDateTime(QDateTime.currentDateTime())
        self.deadline_input.setDisplayFormat("yyyy-MM-dd HH:mm")
        self.status_combo = QComboBox()
        self.status_combo.addItems(self.statuses)

        form_layout.addWidget(self.title_input)
        form_layout.addWidget(self.tag_input)
        form_layout.addWidget(self.deadline_input)
        form_layout.addWidget(self.status_combo)

        add_button = QPushButton("添加任务")
        add_button.clicked.connect(self.add_task)
        form_layout.addWidget(add_button)

        right_layout.addLayout(form_layout)
        main_layout.addLayout(right_layout)
        return main_layout

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if hasattr(self, "_drag_pos") and event.buttons() == Qt.LeftButton:
            delta = event.globalPosition().toPoint() - self._drag_pos
            self.move(self.pos() + delta)
            self._drag_pos = event.globalPosition().toPoint()

# def _init_menu(self):  # 已弃用
        # menubar = self.menuBar()  # 已弃用








    def open_style_dialog(self):
        dlg = StyleSettingsDialog(self)
        dlg.exec()

    def open_language_dialog(self):
        dialog = LanguageDialog()
        if dialog.exec():
            lang = dialog.selected_language()
            set_language(lang)
            QMessageBox.information(self, "提示", f"语言已设置为：{lang}")

    def apply_stylesheet(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            QMessageBox.warning(self, "样式错误", f"无法加载样式表:\n{e}")

    def change_filter(self, index):
        self.current_filter = ["all", "pending", "done"][index]
        self.refresh_list()

    def add_task(self):
        title = self.title_input.text().strip()
        tag = self.tag_input.text().strip()
        deadline = self.deadline_input.dateTime().toPython()
        status = self.status_combo.currentText()
        if not title:
            QMessageBox.warning(self, "错误", "任务标题不能为空！")
            return
        task = Task(title=title, tag=tag, status=status, deadline=deadline)
        self.tasks.append(task)
        self.refresh_list()
        save_tasks(self.tasks)
        self.title_input.clear()
        self.tag_input.clear()
        self.deadline_input.setDateTime(QDateTime.currentDateTime())
        self.status_combo.setCurrentIndex(0)

    def refresh_list(self):
        self.task_list.clear()
        for task in self.tasks:
            if self.current_filter == "pending" and task.status != "pending":
                continue
            if self.current_filter == "done" and task.status != "done":
                continue
            item = QListWidgetItem()
            item.setSizeHint(QSize(200, 50))
            widget = TaskItemWidget(task, self.edit_task)
            self.task_list.addItem(item)
            self.task_list.setItemWidget(item, widget)

    def edit_task(self, task):
        def on_save(updated_task):
            save_tasks(self.tasks)
            self.refresh_list()
        dialog = EditTaskDialog(task, on_save)
        dialog.exec()

    def load(self):
        self.tasks = load_tasks()
        self.refresh_list()

    def mouseReleaseEvent(self, event):
        self._resizing = False
        self._resize_direction = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint()
            self._resize_direction = self._get_resize_direction(event.pos())
            self._resizing = self._resize_direction is not None

    def mouseMoveEvent(self, event):
        if self._resizing:
            self._resize_window(event.globalPosition().toPoint())
        else:
            if event.buttons() == Qt.LeftButton and hasattr(self, "_drag_pos"):
                delta = event.globalPosition().toPoint() - self._drag_pos
                self.move(self.pos() + delta)
                self._drag_pos = event.globalPosition().toPoint()
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

    def _get_resize_direction(self, pos):
        x, y, w, h, m = pos.x(), pos.y(), self.width(), self.height(), self._resize_margin
        if x < m and y < m: return "top_left"
        elif x > w - m and y < m: return "top_right"
        elif x < m and y > h - m: return "bottom_left"
        elif x > w - m and y > h - m: return "bottom_right"
        elif x < m: return "left"
        elif x > w - m: return "right"
        elif y < m: return "top"
        elif y > h - m: return "bottom"
        return None

    def _resize_window(self, global_pos):
        rect = self.geometry()
        diff = global_pos - self.mapToGlobal(QPoint(0, 0))
        if self._resize_direction == "right":
            rect.setWidth(diff.x())
        elif self._resize_direction == "bottom":
            rect.setHeight(diff.y())
        elif self._resize_direction == "bottom_right":
            rect.setWidth(diff.x())
            rect.setHeight(diff.y())
        elif self._resize_direction == "left":
            dx = diff.x()
            rect.setX(rect.x() + dx)
            rect.setWidth(rect.width() - dx)
        elif self._resize_direction == "top":
            dy = diff.y()
            rect.setY(rect.y() + dy)
            rect.setHeight(rect.height() - dy)
        elif self._resize_direction == "top_left":
            dx, dy = diff.x(), diff.y()
            rect.setX(rect.x() + dx)
            rect.setWidth(rect.width() - dx)
            rect.setY(rect.y() + dy)
            rect.setHeight(rect.height() - dy)
        elif self._resize_direction == "top_right":
            dy = diff.y()
            rect.setY(rect.y() + dy)
            rect.setHeight(rect.height() - dy)
            rect.setWidth(diff.x())
        elif self._resize_direction == "bottom_left":
            dx = diff.x()
            rect.setX(rect.x() + dx)
            rect.setWidth(rect.width() - dx)
            rect.setHeight(diff.y())
        self.setGeometry(rect)


    def open_settings_menu(self):
        menu = QMenu(self)
        action_lang = QAction("语言设置", self)
        action_lang.triggered.connect(self.open_language_dialog)
        action_style = QAction("样式设置", self)
        action_style.triggered.connect(self.open_style_dialog)
        menu.addAction(action_lang)
        menu.addAction(action_style)
        button = self.sender()
        menu.exec(button.mapToGlobal(button.rect().bottomLeft()))
