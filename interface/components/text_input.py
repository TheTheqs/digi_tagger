from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout


class TextInput(QWidget):
    def __init__(self, label: str, placeholder: str = ""):
        super().__init__()

        self.input = QLineEdit()
        self.input.setPlaceholderText(placeholder)

        label_widget = QLabel(label)
        label_widget.setStyleSheet("font-weight: bold; margin-bottom: 4px;")

        layout = QVBoxLayout()
        layout.addWidget(label_widget)
        layout.addWidget(self.input)

        self.setLayout(layout)

    def text(self) -> str:
        return self.input.text()

    def set_text(self, value: str):
        self.input.setText(value)