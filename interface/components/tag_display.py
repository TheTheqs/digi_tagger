from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from interface.components.dropdown import Dropdown
from interface.components.tool_button import ToolButton

class TagDisplay(QWidget):
    def __init__(self, tag_type_id: int, tag_type_name: str, tag_items: list[tuple[str, int]], on_add_tag_callback):
        super().__init__()

        self.tag_type_id = tag_type_id
        self.tag_type_name = tag_type_name
        self.on_add_tag_callback = on_add_tag_callback

        layout = QHBoxLayout()

        self.label = QLabel(self.tag_type_name)
        layout.addWidget(self.label)

        self.dropdown = Dropdown(tag_items)  # agora recebe tuplas (name, id)
        layout.addWidget(self.dropdown)

        self.add_button = ToolButton("+", "Adicionar nova Tag", self._on_add_tag)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def _on_add_tag(self):
        self.on_add_tag_callback(self.tag_type_id, self.tag_type_name)

    def update_tags(self, tag_items: list[tuple[str, int]]):
        self.dropdown.set_items(tag_items)

    def get_selected_tag_id(self) -> int | None:
        return self.dropdown.get_selected_id()

    def get_selected_tag(self) -> tuple[int, str]:
        return self.dropdown.get_selected_id(), self.dropdown.get_selected_text()
