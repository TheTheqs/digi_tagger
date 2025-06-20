from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from interface.components.dropdown import Dropdown
from interface.components.tool_button import ToolButton

class TagTypeLayer(QWidget):
    def __init__(self, tag_type_id: int, tag_type_name: str, tag_names: list[str], on_add_tag_callback):
        super().__init__()

        self.tag_type_id = tag_type_id
        self.tag_type_name = tag_type_name
        self.on_add_tag_callback = on_add_tag_callback

        layout = QHBoxLayout()

        self.label = QLabel(self.tag_type_name)
        layout.addWidget(self.label)

        self.dropdown = Dropdown(tag_names)
        layout.addWidget(self.dropdown)

        self.add_button = ToolButton("+", "Adicionar novo Tag", self._on_add_tag)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def _on_add_tag(self):
        self.on_add_tag_callback(self.tag_type_id, self.tag_type_name)
