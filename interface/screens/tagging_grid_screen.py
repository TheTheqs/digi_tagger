# interface/screens/tagging_grid_screen.py

from PySide6.QtWidgets import QWidget, QVBoxLayout
from interface.components.title import Title
from interface.components.back_button import BackButton
from interface.components.loading_screen import LoadingScreen
from interface.components.sprite_grid import SpriteGrid
from interface.components.selectable_sprite import SelectableSprite
from interface.components.custom_button import CustomButton
from interface.components.dropdown import Dropdown
from interface.components.tag_display import TagDisplay
from interface.components.create_tag_popup import CreateTagPopup
from interface.components.create_tag_type_popup import CreateTagTypePopup
from services.application_services import ApplicationService


class TaggingGridScreen(QWidget):
    def __init__(self, navigate_callback, app_service: ApplicationService, update_confirm_screen_callback):
        super().__init__()

        self.navi = navigate_callback
        self.app_service: ApplicationService = app_service
        self.update_confirm_screen = update_confirm_screen_callback
        self.worker = None
        self.loading_widget = LoadingScreen("🧠 Carregando sprites...")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.title = Title("🧩 Curadoria de Sprites")
        self.layout.addWidget(self.title)

        self.back_button = BackButton(lambda: self.navi("home"))
        self.grid = SpriteGrid(sprites_per_row=10)

        self.create_tag_type_button = CustomButton("Criar TagType", self._open_create_tag_type_popup)
        self.layout.addWidget(self.create_tag_type_button)

        self.tag_type_dropdown = Dropdown(self._get_tag_type_options())
        self.tag_type_dropdown.currentIndexChanged.connect(self._on_tag_type_selected)
        self.layout.addWidget(self.tag_type_dropdown)

        self.tag_display = None
        self.proceed_button = None  # será adicionado apenas se tag_display estiver presente

        self._build()

    def _build(self):
        self.layout.addWidget(self.loading_widget)
        self.worker = self.app_service.worker.get_worker(self.load_sprites)
        self.worker.finished.connect(self._on_sprites_loaded)
        self.worker.start()

    def load_sprites(self) -> list[tuple[int, str]]:
        return self.app_service.db.get_all_sprites()

    def _on_sprites_loaded(self, result):
        self.layout.removeWidget(self.loading_widget)
        self.loading_widget.setParent(None)
        self.layout.addWidget(self.back_button)

        if isinstance(result, Exception):
            from interface.components.string_list_box import StringListBox
            error_box = StringListBox([f"[ERRO] Falha ao carregar sprites: {result}"])
            self.layout.addWidget(error_box)
        else:
            sprite_widgets = [
                SelectableSprite(sprite_id=sid, image_path=path, selection_callback=self.grid.on_selection_toggled)
                for sid, path in result
            ]
            self.grid.update_grid(sprite_widgets)
            self.layout.addWidget(self.grid)

    def _get_tag_type_options(self) -> list[tuple[str, int]]:
        tag_types = self.app_service.db.get_all_tag_types()
        return [("<Nenhum TagType selecionado>", -1)] + tag_types

    def _on_tag_type_selected(self):
        tag_type_id = self.tag_type_dropdown.get_selected_id()

        # Remove componentes antigos
        for comp in [self.tag_display, self.proceed_button]:
            if comp:
                self.layout.removeWidget(comp)
                comp.setParent(None)

        self.tag_display = None
        self.proceed_button = None

        if tag_type_id == -1:
            sprites = self.app_service.db.get_all_sprites()
        else:
            sprites = self.app_service.db.get_all_unlabeled_sprite_id_paths(tag_type_id)
            tag_type_name = self.tag_type_dropdown.get_selected_text()
            tag_options = self.app_service.db.get_tags_by_tag_type(tag_type_id)

            self.tag_display = TagDisplay(
                tag_type_id=tag_type_id,
                tag_type_name=tag_type_name,
                tag_items=tag_options,
                on_add_tag_callback=self._on_create_tag
            )
            self.layout.addWidget(self.tag_display)

            self.proceed_button = CustomButton("📤 Prosseguir", self._on_proceed)
            self.layout.addWidget(self.proceed_button)

        sprite_widgets = [
            SelectableSprite(sprite_id=sid, image_path=path, selection_callback=self.grid.on_selection_toggled)
            for sid, path in sprites
        ]
        self.grid.update_grid(sprite_widgets)

    def _on_proceed(self):
        if not self.tag_display:
            return

        tag = self.tag_display.get_selected_tag()
        if not tag:
            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Tag não selecionada", "Por favor, selecione uma tag para continuar.")
            return

        tag_id, tag_name = tag
        tag_type_name = self.tag_display.tag_type_name
        label = f"{tag_type_name}: {tag_name}"

        selected_sprites = self.grid.get_selected_infos()

        self.update_confirm_screen(tag_id, label, selected_sprites)
        self.navi("confirm")

    def _open_create_tag_type_popup(self):
        popup = CreateTagTypePopup(self._create_tag_type)
        popup.exec()

    def _create_tag_type(self, name: str):
        self.app_service.db.create_tag_type(name)
        self.tag_type_dropdown.set_items(self._get_tag_type_options())

    def _on_create_tag(self, tag_type_id: int, tag_type_name: str):
        popup = CreateTagPopup(lambda name: self._create_tag(tag_type_id, tag_type_name, name))
        popup.exec()

    def _create_tag(self, tag_type_id: int, tag_type_name: str, tag_name: str):
        self.app_service.db.create_tag(tag_name=tag_name, tag_type_id=tag_type_id)
        if self.tag_display:
            updated_tags = self.app_service.db.get_tags_by_tag_type(tag_type_id)
            self.tag_display.update_tags(updated_tags)

