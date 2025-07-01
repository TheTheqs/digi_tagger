# interface/components/selectable_sprite.py

from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QSizePolicy
from PySide6.QtGui import QPixmap, QPainter, QColor, QMouseEvent
from PySide6.QtCore import Qt, QRectF


class SelectableSprite(QGraphicsView):
    def __init__(self, sprite_id: int, image_path: str, selected: bool = False,
                 selectable: bool = True,  selection_callback = None):
        super().__init__()

        self.sprite_id = sprite_id
        self.image_path = image_path
        self.selected = selected
        self.selectable = selectable
        self.selection_callback = selection_callback

        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)

        self._image_item = None
        self._scaled_pixmap = None

        self.setRenderHints(self.renderHints() |
                            QPainter.RenderHint.Antialiasing |
                            QPainter.RenderHint.SmoothPixmapTransform)

        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setMinimumSize(96, 96)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self._load_image()

    def _load_image(self):
        self._scene.clear()
        pixmap = QPixmap(self.image_path)

        if not pixmap.isNull():
            self._scaled_pixmap = pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

            self._image_item = QGraphicsPixmapItem(self._scaled_pixmap)
            self._scene.addItem(self._image_item)

            rect = QRectF(self._image_item.boundingRect())
            self._scene.setSceneRect(rect)
            self.centerOn(self._image_item)

    def resizeEvent(self, event):
        self._load_image()
        self.viewport().update()
        super().resizeEvent(event)

    def drawForeground(self, painter, rect):
        if self.selectable and self.selected and self._image_item:
            overlay_color = QColor(0, 255, 0, 60)
            painter.fillRect(self._image_item.boundingRect(), overlay_color)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton and self.selectable:
            self.toggle_selection()
        super().mousePressEvent(event)

    def toggle_selection(self):
        self.selected = not self.selected
        self.viewport().update()
        if callable(self.selection_callback):
            self.selection_callback()

    def get_sprite_id(self):
        return self.sprite_id

    def get_sprite_info(self) -> tuple[int, str]:
        return self.sprite_id, self.image_path

    def is_selected(self):
        return self.selected

    def wheelEvent(self, event):
        event.ignore()