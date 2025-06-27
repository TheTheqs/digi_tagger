from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QSizePolicy
from PySide6.QtGui import QPixmap, QPainter, QPen, QColor
from PySide6.QtCore import Qt, QRectF


class Layer(QGraphicsView):
    def __init__(self):
        super().__init__()

        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)
        self._image_item = None

        # Renderização de qualidade
        self.setRenderHints(self.renderHints() |
                            QPainter.RenderHint.Antialiasing |
                            QPainter.RenderHint.SmoothPixmapTransform)

        # Sem rolagem ou zoom
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Expansível no layout
        self.setMinimumSize(320, 320)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def set_image(self, image_path: str):
        self._scene.clear()
        pixmap = QPixmap(image_path)

        if not pixmap.isNull():
            # Adiciona imagem
            self._image_item = QGraphicsPixmapItem(pixmap)
            self._scene.addItem(self._image_item)

            # Adiciona borda
            rect = QRectF(pixmap.rect())
            pen = QPen(QColor("gray"))
            pen.setWidth(2)
            self._scene.addRect(rect, pen)

            # Ajusta a cena e encaixa imagem na view
            self._scene.setSceneRect(rect)
            self.fitInView(rect, Qt.AspectRatioMode.KeepAspectRatio)
            self.centerOn(self._image_item)
