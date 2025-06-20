from PySide6.QtWidgets import QWidget, QVBoxLayout
from interface.components.title import Title
from interface.components.custom_button import CustomButton
from interface.components.tag_type_list import TagTypeList
from interface.components.tag_type_layer import TagTypeLayer

class TagAdminScreen(QWidget):
    def __init__(self, navigate_callback, app_service):
        super().__init__()

        self.navi = navigate_callback
        self.app_service = app_service

        self.setStyleSheet("padding: 20px;")

        layout = QVBoxLayout()

        title = Title("Administração de Tags e TagTypes")
        layout.addWidget(title)

        btn_create_tag_type = CustomButton("🏷️ Criar nova TagType", self.create_tag_type)
        layout.addWidget(btn_create_tag_type)

        # Novo componente scrollable
        self.tag_type_list = TagTypeList()
        layout.addWidget(self.tag_type_list)

        self.setLayout(layout)

        self.load_tag_types()

    def create_tag_type(self):
        print("Placeholder: criar nova TagType")

    def load_tag_types(self):
        # Exemplo inicial: vamos simular só com alguns dados mockados
        mock_tag_types = [
            ("Tipo 1", ["A", "B", "C"]),
            ("Tipo 2", ["X", "Y"]),
            ("Tipo 3", ["Q", "W", "E", "R", "T"])
        ]

        self.tag_type_list.clear()

        for tag_type_name, tag_names in mock_tag_types:
            layer = TagTypeLayer(tag_type_name, tag_names, self.on_add_tag)
            self.tag_type_list.add_tag_type_layer(layer)

    def on_add_tag(self, tag_type_name):
        print(f"Adicionar tag para {tag_type_name}")
