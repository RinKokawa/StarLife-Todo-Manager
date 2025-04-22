# ui/splash.py
from PySide6.QtWidgets import QSplashScreen, QGraphicsOpacityEffect
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve

def show_splash_then(main_window_callable):
    splash = QSplashScreen(QPixmap("assets/logo.png"))
    splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
    splash.setMask(splash.pixmap().mask())
    splash.showMessage("正在加载 StarLife...", Qt.AlignBottom | Qt.AlignCenter, Qt.white)

    # 设置透明度动画
    effect = QGraphicsOpacityEffect()
    splash.setGraphicsEffect(effect)
    anim = QPropertyAnimation(effect, b"opacity")
    anim.setDuration(800)
    anim.setStartValue(0.0)
    anim.setEndValue(1.0)
    anim.setEasingCurve(QEasingCurve.InOutQuad)
    anim.start()

    splash.show()

    # 延迟显示主窗口
    QTimer.singleShot(1800, lambda: launch_main_window(splash, main_window_callable))

def launch_main_window(splash, main_window_callable):
    splash.close()
    window = main_window_callable()
    window.show()