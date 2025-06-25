# interface/screens/edit_selected_sprite_screen.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QMessageBox
from interface.components.title import Title
from interface.components.back_button import BackButton
from interface.components.custom_button import CustomButton
from interface.components.layer import Layer
from interface.components.tag_display import TagDisplay
from interface.components.tag_display_list import TagDisplayList
from interface.components.text_input import TextInput

class ReviewScreen(QWidget):
    def __init__(self, navigate_callback, app_service):
        super().__init__()

        self.navi = navigate_callback
        self.app_service = app_service

        self.current_sprite = None
        self.tag_displays = []

        self.setStyleSheet("padding: 20px;")

        main_layout = QVBoxLayout()

        # BackButton
        back_button = BackButton(lambda: self.navi("home"))
        main_layout.addWidget(back_button)

        # Title
        title = Title("Edição Manual de Sprite")
        main_layout.addWidget(title)

        # TextInput para digitar o ID do sprite
        self.input_id = TextInput("ID do Sprite:", "Digite o ID e clique em Carregar")
        main_layout.addWidget(self.input_id)

        # Botão para carregar o sprite pelo ID
        btn_load = CustomButton("🔄 Carregar Sprite", self.load_sprite_by_id)
        main_layout.addWidget(btn_load)

        # Layout horizontal com imagem e formulário
        content_layout = QHBoxLayout()

        self.layer = Layer()
        self.layer.setFixedSize(320, 320)
        content_layout.addWidget(self.layer)

        self.tag_display_list = TagDisplayList()
        content_layout.addWidget(self.tag_display_list)

        main_layout.addLayout(content_layout)

        # Botão de salvar
        btn_save = CustomButton("💾 Salvar Classificação", self.save_configuration)
        main_layout.addWidget(btn_save)

        self.setLayout(main_layout)

    def load_sprite_by_id(self):
        sprite_id_text = self.input_id.text()
        if not sprite_id_text.isdigit():
            QMessageBox.warning(self, "Entrada inválida", "Digite um ID numérico válido.")
            return

        sprite_id = int(sprite_id_text)

        # Limpa o formulário
        self.tag_display_list.clear()
        self.tag_displays.clear()

        sprite = self.app_service.db.get_sprite_by_id(sprite_id)
        if not sprite:
            QMessageBox.warning(self, "Não encontrado", f"Sprite com ID {sprite_id} não encontrado.")
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
            # Atualiza só o dropdown deste tag_display:
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

        self.app_service.db.save_configuration_for_sprite(self.current_sprite.id, tag_ids)
        QMessageBox.information(self, "Sucesso", "Classificação salva com sucesso!")
        self.navi("home")
