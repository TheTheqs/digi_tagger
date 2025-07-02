# interface/components/loading_screen.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QMovie
from interface.components.title import Title


class LoadingScreen(QWidget):
    def __init__(self, message="Loading..."):
        super().__init__()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        # Title
        self.title = Title(message)
        layout.addWidget(self.title)

        # Animation
        self.loading_label = QLabel()
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.movie = QMovie("assets/loader.gif")
        self.loading_label.setMovie(self.movie)
        self.movie.start()

        layout.addWidget(self.loading_label)
        self.setLayout(layout)

    def set_message(self, message: str):
        """
        Atualiza a mensagem exibida no título da tela de loading.
        """
        self.title.setText(message)