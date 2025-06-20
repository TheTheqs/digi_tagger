from PySide6.QtWidgets import QComboBox

class Dropdown(QComboBox):
    def __init__(self, options: list[str] = None):
        super().__init__()

        if options:
            self.add_items(options)

    def add_items(self, options: list[str]):
        self.clear()
        self.addItems(options)

    def get_selected_text(self) -> str:
        return self.currentText()

    def get_selected_index(self) -> int:
        return self.currentIndex()
