from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt


class Title(QLabel):
    def __init__(self, text: str):
        super().__init__(text)

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 20px;
        """)