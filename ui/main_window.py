# ui/main_window.py
import os
from pathlib import Path
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QListWidget, QListWidgetItem,
    QMessageBox, QDateTimeEdit, QComboBox, QLabel, QMenuBar, QMenu, QFileDialog
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QDateTime, QSize
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
        self.tasks = []
        self.statuses = load_statuses()
        self.current_filter = "all"
        self.init_ui()
        self.load()

    def init_ui(self):
        self._init_menu()

        central_widget = QWidget()
        main_layout = QHBoxLayout()

        # 左侧菜单栏
        self.menu_list = QListWidget()
        self.menu_list.addItem("📋 所有任务")
        self.menu_list.addItem("⏳ 未完成任务")
        self.menu_list.addItem("✅ 已完成任务")
        self.menu_list.setFixedWidth(120)
        self.menu_list.currentRowChanged.connect(self.change_filter)
        main_layout.addWidget(self.menu_list)

        # 右侧主内容区
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

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # ✅ 设置默认筛选
        self.menu_list.setCurrentRow(0)

        # ✅ 默认加载样式
        self.apply_stylesheet("assets/style.qss")



    # 方法
    def open_style_dialog(self):
        dlg = StyleSettingsDialog(self)
        dlg.exec()

    def _init_menu(self):
        menubar = self.menuBar()
        settings_menu = menubar.addMenu("设置")

        lang_action = QAction("语言", self)
        lang_action.triggered.connect(self.open_language_dialog)
        settings_menu.addAction(lang_action)

        style_action = QAction("样式设置", self)
        style_action.triggered.connect(self.open_style_dialog)
        settings_menu.addAction(style_action)


    def open_language_dialog(self):
        dialog = LanguageDialog()
        if dialog.exec():
            lang = dialog.selected_language()
            set_language(lang)
            QMessageBox.information(self, "提示", f"语言已设置为：{lang}")

    def load_stylesheet_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择样式表", "", "QSS 文件 (*.qss)")
        if file_path:
            self.apply_stylesheet(file_path)

    def apply_stylesheet(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            QMessageBox.warning(self, "样式错误", f"无法加载样式表:\n{e}")

    def change_filter(self, index):
        if index == 0:
            self.current_filter = "all"
        elif index == 1:
            self.current_filter = "pending"
        elif index == 2:
            self.current_filter = "done"
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