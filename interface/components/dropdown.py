from PySide6.QtWidgets import QComboBox

class Dropdown(QComboBox):
    def __init__(self, options: list[tuple[str, int]] = None):
        """
        options: lista de tuplas (nome_visivel, id_interno)
        """
        super().__init__()
        if options:
            self.set_items(options)  # usa o novo alias

    def add_items(self, options: list[tuple[str, int]]):
        for name, value in options:
            self.addItem(name, userData=value)

    def set_items(self, options: list[tuple[str, int]]):
        """Limpa o dropdown e define novos itens"""
        self.clear()
        self.add_items(options)

    def get_selected_text(self) -> str:
        return self.currentText()

    def get_selected_index(self) -> int:
        return self.currentIndex()

    def get_selected_id(self) -> int:
        return self.currentData()

    def wheelEvent(self, event):
        event.ignore()