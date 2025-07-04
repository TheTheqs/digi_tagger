from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from interface.components.dropdown import Dropdown
from interface.components.tool_button import ToolButton
from database.dtos import TagTypeResponseDTO, TagResponseDTO

class TagDisplay(QWidget):
    def __init__(self, tag_type: TagTypeResponseDTO, tags: list[TagResponseDTO], on_add_tag_callback):
        super().__init__()

        self.tag_type = tag_type
        self.tags = tags
        self.on_add_tag_callback = on_add_tag_callback

        layout = QHBoxLayout()

        # Label com nome do tipo de tag
        self.label = QLabel(self.tag_type.name)
        layout.addWidget(self.label)

        # Dropdown usando name como label e id como value
        self.dropdown = Dropdown([(tag.name, tag.id) for tag in self.tags])
        layout.addWidget(self.dropdown)

        # Botão para adicionar nova tag
        self.add_button = ToolButton("+", "Adicionar nova Tag", self._on_add_tag)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def _on_add_tag(self):
        self.on_add_tag_callback(self.tag_type)

    def update_tags(self, new_tags: list[TagResponseDTO]):
        self.tags = new_tags
        self.dropdown.set_items([(tag.name, tag.id) for tag in new_tags])

    def get_selected_tag_id(self) -> int | None:
        return self.dropdown.get_selected_id()

    def get_selected_tag(self) -> TagResponseDTO | None:
        selected_id = self.get_selected_tag_id()
        return next((tag for tag in self.tags if tag.id == selected_id), None)
