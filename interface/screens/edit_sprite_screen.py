from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QMessageBox
from interface.components.title import Title
from interface.components.back_button import BackButton
from interface.components.custom_button import CustomButton
from interface.components.layer import Layer
from interface.components.tag_display import TagDisplay
from interface.components.tag_display_list import TagDisplayList
from services.application_services import ApplicationService


class EditSpriteScreen(QWidget):
    def __init__(self, navigate_callback, app_service: ApplicationService):
        super().__init__()

        self.navi = navigate_callback
        self.app_service: ApplicationService = app_service

        self.current_sprite = None
        self.tag_displays = []

        self.setStyleSheet("padding: 20px;")
        main_layout = QVBoxLayout()

        # Botão de voltar
        back_button = BackButton(lambda: self.navi("home"))
        main_layout.addWidget(back_button)

        # Título
        title = Title("Classificação de Sprite")
        main_layout.addWidget(title)

        # Layout horizontal com imagem + form de tags
        content_layout = QHBoxLayout()

        # Imagem
        self.layer = Layer()
        self.layer.setFixedSize(320, 320)
        content_layout.addWidget(self.layer)

        # Dropdowns de tags
        self.tag_display_list = TagDisplayList()
        content_layout.addWidget(self.tag_display_list)

        main_layout.addLayout(content_layout)

        # Botão salvar
        btn_save = CustomButton("💾 Salvar Classificação", self.save_configuration)
        main_layout.addWidget(btn_save)

        self.setLayout(main_layout)
        self.load_next_sprite()

    def load_next_sprite(self):
        self.tag_display_list.clear()
        self.tag_displays.clear()

        sprite = self.app_service.db.get_next_unedited_sprite()
        if not sprite:
            QMessageBox.information(self, "Parabéns!", "Todos os sprites foram classificados!")
            self.navi("home")
            return

        self.current_sprite = sprite
        self.layer.set_image(sprite.path)

        tag_type_ids = self.app_service.db.get_all_tag_type_ids()

        for tag_type_id in tag_type_ids:
            tag_type_name, tag_names = self.app_service.db.get_tag_type_with_tags(tag_type_id)
            tag_display = TagDisplay(
                tag_type_id,
                tag_type_name,
                tag_names,
                self.on_add_tag
            )
            self.tag_display_list.add_tag_display(tag_display)
            self.tag_displays.append(tag_display)

    def on_add_tag(self, tag_type_id: int, tag_type_name: str):
        def on_save(tag_name):
            self.app_service.db.create_tag(tag_name, tag_type_id)
            tag_display = next((td for td in self.tag_displays if td.tag_type_id == tag_type_id), None)
            if tag_display:
                _, tag_names = self.app_service.db.get_tag_type_with_tags(tag_type_id)
                tag_display.update_tags(tag_names)

        from interface.components.create_tag_popup import CreateTagPopup
        popup = CreateTagPopup(on_save)
        popup.exec()

    def save_configuration(self):
        tag_ids = []
        tag_type_ids_collected = set()

        for tag_display in self.tag_displays:
            selected_tag_name = tag_display.dropdown.currentText()
            if not selected_tag_name:
                QMessageBox.warning(self, "Validação", "Todas as categorias devem ter uma tag selecionada.")
                return

            tag_id = self.app_service.db.get_tag_id_by_name(selected_tag_name, tag_display.tag_type_id)
            tag_ids.append(tag_id)
            tag_type_ids_collected.add(tag_display.tag_type_id)

        all_tag_type_ids = self.app_service.db.get_all_tag_type_ids()
        if set(all_tag_type_ids) != tag_type_ids_collected:
            QMessageBox.warning(self, "Validação", "Nem todas as categorias foram preenchidas corretamente.")
            return

        for tag_id in tag_ids:
            self.app_service.db.add_tag_to_sprite(self.current_sprite.id, tag_id)

        self.app_service.db.mark_sprite_as_edited(self.current_sprite.id)

        QMessageBox.information(self, "Sucesso", "Classificação salva com sucesso!")
        self.navi("home")
