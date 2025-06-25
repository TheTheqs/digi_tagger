from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PySide6.QtGui import QPixmap, QWheelEvent, QPainter
from PySide6.QtCore import Qt


class Layer(QGraphicsView):
    def __init__(self):
        super().__init__()
        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)

        self._image_item = None
        self._zoom = 1.0
        self._zoom_step = 0.1
        self._min_zoom = 0.2
        self._max_zoom = 3.0

        self.setRenderHints(self.renderHints() |
                            QPainter.RenderHint.Antialiasing |
                            QPainter.RenderHint.SmoothPixmapTransform)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def set_image(self, image_path: str):
        self._scene.clear()
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            self._image_item = QGraphicsPixmapItem(pixmap)
            self._scene.addItem(self._image_item)
            self._zoom = 1.0
            self.resetTransform()
            self.centerOn(self._image_item)

    def wheelEvent(self, event: QWheelEvent):
        delta = event.angleDelta().y()
        if delta > 0 and self._zoom < self._max_zoom:
            self._zoom += self._zoom_step
        elif delta < 0 and self._zoom > self._min_zoom:
            self._zoom -= self._zoom_step
        else:
            return

        self.resetTransform()
        self.scale(self._zoom, self._zoom)
        if self._image_item:
            self.centerOn(self._image_item)