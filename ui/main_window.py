
import os
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
        self.init_ui()
        self.load()

    def init_ui(self):
        self._init_menu()
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

        btn_min = QPushButton("—")
        btn_min.clicked.connect(self.showMinimized)

        btn_close = QPushButton("×")
        btn_close.clicked.connect(self.close)

        layout.addWidget(title)
        layout.addStretch()
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

    def _init_menu(self):
        menubar = self.menuBar()
        settings_menu = menubar.addMenu("设置")
        lang_action = QAction("语言", self)
        lang_action.triggered.connect(self.open_language_dialog)
        settings_menu.addAction(lang_action)
        style_action = QAction("样式设置", self)
        style_action.triggered.connect(self.open_style_dialog)
        settings_menu.addAction(style_action)

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
