# core/model.py
from datetime import datetime

class Task:
    def __init__(self, title, tag, status, deadline, created=None, subtasks=None):
        self.created = created or datetime.now()
        self.title = title
        self.tag = tag
        self.status = status
        self.deadline = deadline
        self.subtasks = subtasks or []  # list of tuples (str, bool)

    def __str__(self):
        deadline_str = self.deadline.strftime('%Y-%m-%d %H:%M') if self.deadline else ""
        subtask_str = ';;'.join([f"{text}:::{str(done).lower()}" for text, done in self.subtasks])
        return f"[{self.created.strftime('%Y-%m-%d %H:%M')}] title: {self.title} | tag: {self.tag} | status: {self.status} | deadline: {deadline_str} | subtasks: {subtask_str}"

    @staticmethod
    def from_line(line):
        parts = line.strip().split('|')
        created = datetime.strptime(parts[0].split(']')[0][1:], '%Y-%m-%d %H:%M')
        title = parts[0].split('title: ')[1].strip()
        tag = parts[1].split('tag: ')[1].strip()
        status = parts[2].split('status: ')[1].strip()
        deadline_part = parts[3].split('deadline: ')[1].strip()
        deadline = datetime.strptime(deadline_part, '%Y-%m-%d %H:%M') if deadline_part else None
        subtasks = []
        if len(parts) > 4 and 'subtasks:' in parts[4]:
            subtask_data = parts[4].split('subtasks:')[1].strip()
            for sub in subtask_data.split(';;'):
                if ':::' in sub:
                    text, done = sub.split(':::')
                    subtasks.append((text.strip(), done.strip().lower() == 'true'))
        return Task(title, tag, status, deadline, created, subtasks)
