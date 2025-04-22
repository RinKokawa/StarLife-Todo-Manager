# StarLife Todo Manager

An elegant desktop task manager built with Python and PySide6. It supports multi-language UI, sub-tasks, dynamic themes, and persistent local storage.

## ✨ Features

- ✅ Add / Edit / Delete tasks
- 🗂 Task filtering (All / Pending / Done)
- 🌍 Multi-language support (中文 / English / 日本語 / 한국어)
- 🎨 Custom QSS stylesheet loading
- 📝 Subtask system to break big tasks down
- 💾 Configurable local JSON-based storage

## 📦 Install Dependencies

```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple PySide6
```

## 🚀 Run the App

```bash
python main.py
```

## 📁 Project Structure

```
.
├── main.py
├── core/         # Models & storage & config
├── ui/           # UI logic & dialogs & widgets
├── assets/       # Stylesheets & icons
└── .stodolist/   # Local data and configuration
```

## 🔧 Developer Notes

- Default theme file: `assets/style.qss`
- Language setting is stored in `~/.stodolist/config.json`

---

If you enjoy StarLife, give it a ⭐ star to support the project!
