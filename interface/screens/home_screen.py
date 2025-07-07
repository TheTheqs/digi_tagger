from PySide6.QtWidgets import QWidget, QVBoxLayout
from interface.components.title import Title
from interface.components.custom_button import CustomButton


class HomeScreen(QWidget):
    def __init__(self, callback):
        super().__init__()
        self.navi = callback
        self.setStyleSheet("padding: 20px;")

        layout = QVBoxLayout()

        # Title
        title = Title("Welcome to DigiScrap!")
        layout.addWidget(title)

        # Buttons
        btn_scrap= CustomButton("🔍 Autalizar Banco de Dados", lambda: self.navi("update"))
        layout.addWidget(btn_scrap)
        btn_tagging = CustomButton("🖼️ Curadoria Assistida", lambda: self.navi("tagging"))
        layout.addWidget(btn_tagging)
        btn_review = CustomButton("🎨 Revisar Tags", lambda: self.navi("review"))
        layout.addWidget(btn_review)
        btn_analyse = CustomButton("📊 Análise de Dados", lambda: self.navi("data"))
        layout.addWidget(btn_analyse)

        layout.addStretch()
        self.setLayout(layout)
