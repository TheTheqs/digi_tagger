from PySide6.QtWidgets import QWidget, QVBoxLayout
from interface.components.title import Title
from interface.components.custom_button import CustomButton
from interface.components.tag_type_list import TagTypeList
from interface.components.tag_type_layer import TagTypeLayer
from interface.components.create_tag_type_popup import CreateTagTypePopup
from interface.components.create_tag_popup import CreateTagPopup
from interface.components.back_button import BackButton  # <-- Aqui incluímos o seu componente!
from services.application_services import ApplicationService

class TagAdminScreen(QWidget):
    def __init__(self, navigate_callback, app_service: ApplicationService):
        super().__init__()

        self.navi = navigate_callback
        self.app_service: ApplicationService = app_service

        self.setStyleSheet("padding: 20px;")

        layout = QVBoxLayout()

        # Botão de voltar
        back_button = BackButton(lambda: self.navi("home"))
        layout.addWidget(back_button)

        title = Title("Administração de Tags e TagTypes")
        layout.addWidget(title)

        btn_create_tag_type = CustomButton("🏷️ Criar nova TagType", self.create_tag_type)
        layout.addWidget(btn_create_tag_type)

        self.tag_type_list = TagTypeList()
        layout.addWidget(self.tag_type_list)

        self.setLayout(layout)

        self.load_tag_types()

    def create_tag_type(self):
        def on_save(name, exclusive):
            self.app_service.db.create_tag_type(name, exclusive)
            self.load_tag_types()

        popup = CreateTagTypePopup(on_save)
        popup.exec()

    def load_tag_types(self):
        self.tag_type_list.clear()
        tag_type_ids = self.app_service.db.get_all_tag_type_ids()

        for tag_type_id in tag_type_ids:
            tag_type_name, tag_names = self.app_service.db.get_tag_type_with_tags(tag_type_id)
            layer = TagTypeLayer(tag_type_id, tag_type_name, tag_names, self.on_add_tag)
            self.tag_type_list.add_tag_type_layer(layer)

    def on_add_tag(self, tag_type_id: int, tag_type_name: str):
        def on_save(tag_name):
            self.app_service.db.create_tag(tag_name, tag_type_id)
            self.load_tag_types()

        popup = CreateTagPopup(on_save)
        popup.exec()
