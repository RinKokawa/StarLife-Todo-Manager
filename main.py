from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from core.config import apply_stylesheet
from ui.splash import show_splash_then

if __name__ == "__main__":
    app = QApplication([])
    apply_stylesheet(app)
    show_splash_then(MainWindow)
    app.exec()
