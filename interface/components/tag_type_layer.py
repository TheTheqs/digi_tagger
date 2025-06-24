# interface/components/tag_type_layer.py

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from interface.components.dropdown import Dropdown
from interface.components.tool_button import ToolButton

class TagTypeLayer(QWidget):
    def __init__(
        self,
        tag_type_id: int,
        tag_type_name: str,
        tag_names: list[str],
        on_add_tag_callback,
        on_request_delete_tag_type_callback,
        on_request_delete_tag_callback
    ):
        super().__init__()

        self.tag_type_id = tag_type_id
        self.tag_type_name = tag_type_name
        self.on_add_tag_callback = on_add_tag_callback
        self.on_request_delete_tag_type_callback = on_request_delete_tag_type_callback
        self.on_request_delete_tag_callback = on_request_delete_tag_callback

        layout = QHBoxLayout()

        self.label = QLabel(self.tag_type_name)
        layout.addWidget(self.label)

        self.dropdown = Dropdown(tag_names)
        layout.addWidget(self.dropdown)

        self.add_button = ToolButton("+", "Adicionar novo Tag", self._on_add_tag)
        layout.addWidget(self.add_button)

        self.delete_tag_type_button = ToolButton("🗑️", "Deletar TagType", self._on_delete_tag_type)
        layout.addWidget(self.delete_tag_type_button)

        self.delete_tag_button = ToolButton("❌", "Deletar Tag Selecionado", self._on_delete_tag)
        layout.addWidget(self.delete_tag_button)

        self.setLayout(layout)

    def _on_add_tag(self):
        self.on_add_tag_callback(self.tag_type_id, self.tag_type_name)

    def _on_delete_tag_type(self):
        self.on_request_delete_tag_type_callback(self.tag_type_id)

    def _on_delete_tag(self):
        selected_tag = self.dropdown.currentText()
        if selected_tag:
            self.on_request_delete_tag_callback(selected_tag, self.tag_type_id)
