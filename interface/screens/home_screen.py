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
        btn_analyse = CustomButton("📊 Análise de Dados", lambda: self.navi("analyse"))
        layout.addWidget(btn_analyse)
        btn_edit = CustomButton("🖼️ Classificar Próximo Sprite", lambda: self.navi("edit"))
        layout.addWidget(btn_edit)

        layout.addStretch()
        self.setLayout(layout)
