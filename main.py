from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from core.config import apply_stylesheet

if __name__ == "__main__":
    app = QApplication([])
    apply_stylesheet(app)
    win = MainWindow()
    win.show()
    app.exec()
