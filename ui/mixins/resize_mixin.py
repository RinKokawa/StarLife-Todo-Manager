from PySide6.QtCore import QPoint, Qt

class ResizeMixin:
    def __init__(self):
        self._resize_margin = 5
        self._resizing = False
        self._resize_direction = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint()
            self._resize_direction = self._get_resize_direction(event.pos())
            self._resizing = self._resize_direction is not None

    def mouseMoveEvent(self, event):
        if self._resizing:
            self._resize_window(event.globalPosition().toPoint())
        else:
            direction = self._get_resize_direction(event.pos())
            if direction:
                cursors = {
                    "left": Qt.SizeHorCursor,
                    "right": Qt.SizeHorCursor,
                    "top": Qt.SizeVerCursor,
                    "bottom": Qt.SizeVerCursor,
                    "top_left": Qt.SizeFDiagCursor,
                    "top_right": Qt.SizeBDiagCursor,
                    "bottom_left": Qt.SizeBDiagCursor,
                    "bottom_right": Qt.SizeFDiagCursor,
                }
                self.setCursor(cursors[direction])
            else:
                self.setCursor(Qt.ArrowCursor)

    def mouseReleaseEvent(self, event):
        self._resizing = False
        self._resize_direction = None

    def _get_resize_direction(self, pos):
        x, y, w, h, m = pos.x(), pos.y(), self.width(), self.height(), self._resize_margin
        if x < m and y < m: return "top_left"
        elif x > w - m and y < m: return "top_right"
        elif x < m and y > h - m: return "bottom_left"
        elif x > w - m and y > h - m: return "bottom_right"
        elif x < m: return "left"
        elif x > w - m: return "right"
        elif y < m: return "top"
        elif y > h - m: return "bottom"
        return None

    def _resize_window(self, global_pos):
        rect = self.geometry()
        diff = global_pos - self.mapToGlobal(QPoint(0, 0))
        if self._resize_direction == "right":
            rect.setWidth(diff.x())
        elif self._resize_direction == "bottom":
            rect.setHeight(diff.y())
        elif self._resize_direction == "bottom_right":
            rect.setWidth(diff.x())
            rect.setHeight(diff.y())
        elif self._resize_direction == "left":
            dx = diff.x()
            rect.setX(rect.x() + dx)
            rect.setWidth(rect.width() - dx)
        elif self._resize_direction == "top":
            dy = diff.y()
            rect.setY(rect.y() + dy)
            rect.setHeight(rect.height() - dy)
        elif self._resize_direction == "top_left":
            dx, dy = diff.x(), diff.y()
            rect.setX(rect.x() + dx)
            rect.setWidth(rect.width() - dx)
            rect.setY(rect.y() + dy)
            rect.setHeight(rect.height() - dy)
        elif self._resize_direction == "top_right":
            dy = diff.y()
            rect.setY(rect.y() + dy)
            rect.setHeight(rect.height() - dy)
            rect.setWidth(diff.x())
        elif self._resize_direction == "bottom_left":
            dx = diff.x()
            rect.setX(rect.x() + dx)
            rect.setWidth(rect.width() - dx)
            rect.setHeight(diff.y())
        self.setGeometry(rect)
