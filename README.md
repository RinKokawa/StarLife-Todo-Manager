# StarLife Todo Manager

一个优雅的桌面待办事项管理器，支持多语言、子任务、样式切换，基于 Python + PySide6 开发。

## ✨ 功能特色

- ✅ 添加 / 编辑 / 删除任务
- 🗂 任务分类筛选（所有 / 未完成 / 已完成）
- 🌍 多语言支持（中文 / English / 日本語 / 한국어）
- 🔧 自定义主题样式（支持 .qss 样式表）
- 📝 子任务系统，任务更易拆解
- 💾 本地存储，支持自定义配置

## 📦 安装依赖

```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple PySide6
```

## 🚀 启动项目

```bash
python main.py
```

## 📁 项目结构

```
.
├── main.py
├── core/         # 模型 & 存储 & 配置
├── ui/           # 界面逻辑 & 控件 & 弹窗
├── assets/       # 样式文件、图标等
└── .stodolist/   # 用户数据和配置（自动生成）
```

## 🔖 开发者提示

- 默认样式文件位于 `assets/style.qss`
- 多语言配置保存在 `~/.stodolist/config.json`

---

如果你觉得 StarLife 好用，不妨点个 ⭐Star 支持一下！
