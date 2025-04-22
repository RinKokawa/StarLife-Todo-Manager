
# core/storage.py
from pathlib import Path
from core.model import Task

DATA_PATH = Path.home() / ".stodolist"
DATA_FILE = DATA_PATH / "tasks.stodo"

def load_tasks():
    tasks = []
    if not DATA_PATH.exists():
        DATA_PATH.mkdir()
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        tasks.append(Task.from_line(line))
                    except Exception as e:
                        print(f"跳过错误行: {line.strip()} ({e})")
    return tasks

def save_tasks(tasks):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        for task in tasks:
            f.write(str(task) + '\n')