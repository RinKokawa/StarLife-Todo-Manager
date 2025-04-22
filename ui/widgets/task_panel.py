
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QLineEdit, QDateTimeEdit, QComboBox, QPushButton
from PySide6.QtCore import QDateTime, QSize
from core.model import Task
from core.storage import save_tasks
from ui.widgets.task_item_widget import TaskItemWidget

class TaskPanel(QWidget):
    def __init__(self, parent, statuses):
        super().__init__(parent)
        self.parent = parent
        self.statuses = statuses
        self.current_filter = "all"
        self.tasks = []

        layout = QHBoxLayout(self)

        self.menu_list = QListWidget()
        self.menu_list.addItem("📋 所有任务")
        self.menu_list.addItem("⏳ 未完成任务")
        self.menu_list.addItem("✅ 已完成任务")
        self.menu_list.setFixedWidth(120)
        self.menu_list.currentRowChanged.connect(self.change_filter)
        layout.addWidget(self.menu_list)

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
        self.status_combo.addItems(statuses)

        form_layout.addWidget(self.title_input)
        form_layout.addWidget(self.tag_input)
        form_layout.addWidget(self.deadline_input)
        form_layout.addWidget(self.status_combo)

        add_button = QPushButton("添加任务")
        add_button.clicked.connect(self.add_task)
        form_layout.addWidget(add_button)

        right_layout.addLayout(form_layout)
        layout.addLayout(right_layout)

    def set_tasks(self, tasks):
        self.tasks = tasks
        self.refresh_list()

    def change_filter(self, index):
        self.current_filter = ["all", "pending", "done"][index]
        self.refresh_list()

    def refresh_list(self):
        self.task_list.clear()
        for task in self.tasks:
            if self.current_filter == "pending" and task.status != "pending":
                continue
            if self.current_filter == "done" and task.status != "done":
                continue
            item = QListWidgetItem()
            item.setSizeHint(QSize(200, 50))
            widget = TaskItemWidget(task, self.parent.edit_task)
            self.task_list.addItem(item)
            self.task_list.setItemWidget(item, widget)

    def add_task(self):
        title = self.title_input.text().strip()
        tag = self.tag_input.text().strip()
        deadline = self.deadline_input.dateTime().toPython()
        status = self.status_combo.currentText()
        if not title:
            return
        task = Task(title=title, tag=tag, status=status, deadline=deadline)
        self.tasks.append(task)
        self.refresh_list()
        save_tasks(self.tasks)
        self.title_input.clear()
        self.tag_input.clear()
        self.deadline_input.setDateTime(QDateTime.currentDateTime())
        self.status_combo.setCurrentIndex(0)
