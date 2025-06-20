from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt


class ToolButton(QPushButton):
    def __init__(self, icon_text: str, description: str, on_click):
        super().__init__(icon_text)

        self.setToolTip(description)
        self.clicked.connect(on_click)

        self.setFixedSize(40, 40)
        self.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                background-color: #ecf0f1;
                border: 1px solid #bdc3c7;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #d0d3d4;
            }
            QPushButton:pressed {
                background-color: #b2babb;
            }
        """)
        self.setCursor(Qt.CursorShape.PointingHandCursor)