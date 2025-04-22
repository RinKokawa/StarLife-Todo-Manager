# ui/dialogs/edit_task_dialog.py
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QDateTimeEdit, QComboBox, QPushButton, QCheckBox, QWidget, QListWidget,
    QListWidgetItem, QMessageBox
)
from PySide6.QtCore import QDateTime
from core.config import load_statuses

class EditTaskDialog(QDialog):
    def __init__(self, task, on_save):
        super().__init__()
        self.task = task
        self.on_save = on_save
        self.setWindowTitle("编辑任务")
        self.statuses = load_statuses()
        self.subtask_widgets = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.title_input = QLineEdit(self.task.title)
        self.tag_input = QLineEdit(self.task.tag)
        self.deadline_input = QDateTimeEdit()
        self.deadline_input.setCalendarPopup(True)
        self.deadline_input.setDateTime(QDateTime.fromString(self.task.deadline.strftime('%Y-%m-%d %H:%M'), 'yyyy-MM-dd HH:mm'))
        self.deadline_input.setDisplayFormat("yyyy-MM-dd HH:mm")

        self.status_combo = QComboBox()
        self.status_combo.addItems(self.statuses)
        if self.task.status in self.statuses:
            self.status_combo.setCurrentText(self.task.status)

        layout.addWidget(QLabel("标题"))
        layout.addWidget(self.title_input)
        layout.addWidget(QLabel("标签"))
        layout.addWidget(self.tag_input)
        layout.addWidget(QLabel("截止时间"))
        layout.addWidget(self.deadline_input)
        layout.addWidget(QLabel("状态"))
        layout.addWidget(self.status_combo)

        layout.addWidget(QLabel("子任务"))
        self.subtask_list = QVBoxLayout()
        for text, done in self.task.subtasks:
            self.add_subtask_row(text, done)

        self.subtask_container = QWidget()
        self.subtask_container.setLayout(self.subtask_list)
        layout.addWidget(self.subtask_container)

        add_sub_btn = QPushButton("添加子任务")
        add_sub_btn.clicked.connect(lambda: self.add_subtask_row("", False))
        layout.addWidget(add_sub_btn)

        btn_layout = QHBoxLayout()
        save_btn = QPushButton("保存")
        cancel_btn = QPushButton("取消")
        save_btn.clicked.connect(self.save)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def add_subtask_row(self, text, done):
        row = QHBoxLayout()
        checkbox = QCheckBox()
        checkbox.setChecked(done)
        line_edit = QLineEdit(text)
        delete_btn = QPushButton("删除")
        def delete():
            for i in reversed(range(row.count())):
                widget = row.itemAt(i).widget()
                if widget:
                    widget.setParent(None)
            self.subtask_list.removeItem(row)
            self.subtask_widgets.remove((checkbox, line_edit))
        delete_btn.clicked.connect(delete)
        row.addWidget(checkbox)
        row.addWidget(line_edit)
        row.addWidget(delete_btn)
        self.subtask_list.addLayout(row)
        self.subtask_widgets.append((checkbox, line_edit))

    def save(self):
        self.task.title = self.title_input.text().strip()
        self.task.tag = self.tag_input.text().strip()
        self.task.deadline = self.deadline_input.dateTime().toPython()
        self.task.status = self.status_combo.currentText()
        self.task.subtasks = []
        for checkbox, line_edit in self.subtask_widgets:
            text = line_edit.text().strip()
            if text:
                self.task.subtasks.append((text, checkbox.isChecked()))
        self.on_save(self.task)
        self.accept()
