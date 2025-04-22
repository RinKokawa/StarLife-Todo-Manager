# main.py
import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from core.config import init_config

if __name__ == '__main__':
    init_config()
    app = QApplication(sys.argv)
    win = MainWindow()
    win.resize(900, 400)
    win.show()
    sys.exit(app.exec())