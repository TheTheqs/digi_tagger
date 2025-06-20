from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea

class TagTypeList(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        layout.addWidget(self.scroll_area)

        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setSpacing(10)
        self.container_layout.addStretch()  # Sempre empurra para cima

        self.scroll_area.setWidget(self.container)

    def clear(self):
        while self.container_layout.count() > 1:
            item = self.container_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

    def add_tag_type_layer(self, tag_type_layer: QWidget):
        self.container_layout.insertWidget(self.container_layout.count() - 1, tag_type_layer)
