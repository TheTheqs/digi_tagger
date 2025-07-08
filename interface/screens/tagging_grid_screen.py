# interface/screens/tagging_grid_screen.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox
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
from interface.components.string_list_box import StringListBox
from interface.components.tool_button import ToolButton
from services.application_services import ApplicationService
from interface.screens.managers.tagging_data_manager import TaggingDataManager


class TaggingGridScreen(QWidget):
    def __init__(self, navigate_callback, app_service: ApplicationService, update_confirm_screen_callback):
        super().__init__()

        self.navi = navigate_callback
        self.app_service = app_service
        self.update_confirm_screen = update_confirm_screen_callback
        self.manager = TaggingDataManager(app_service.db, app_service.assist)
        self.current_sprites = []

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.title = Title("\U0001F9E9 Curadoria de Sprites")
        self.layout.addWidget(self.title)

        self.back_button = BackButton(lambda: self.navi("home"))
        self.grid = SpriteGrid(sprites_per_row=10)

        self.create_tag_type_button = CustomButton("Criar TagType", self._open_create_tag_type_popup)
        self.layout.addWidget(self.create_tag_type_button)

        # Layout horizontal para os controles superiores
        controls_layout = QHBoxLayout()

        # Dropdown 1 – Seleção do TagType
        self.tag_type_dropdown = Dropdown([("\U0001F552 Carregando tipos de tag...", -1)])
        self.tag_type_dropdown.setMinimumWidth(200)
        self.tag_type_dropdown.currentIndexChanged.connect(self._on_tag_type_selected)
        controls_layout.addWidget(self.tag_type_dropdown)

        # Dropdown 2 – Filtro geral
        self.filter_dropdown = Dropdown([("\U0001F50E Filtrar por tag (qualquer tipo)", -1)])
        self.filter_dropdown.setMinimumWidth(200)
        self.filter_dropdown.currentIndexChanged.connect(self._on_filter_tag_selected)
        controls_layout.addWidget(self.filter_dropdown)

        # Dropdown 3 – Curadoria assistida
        self.assist_dropdown = Dropdown([("\U0001F916 Curadoria assistida por similaridade", -1)])
        self.assist_dropdown.setMinimumWidth(200)
        self.assist_dropdown.currentIndexChanged.connect(self._on_assist_tag_selected)
        controls_layout.addWidget(self.assist_dropdown)

        # Campo de quantidade top_k para curadoria
        topk_label = QLabel("Top-K:")
        self.top_k_input = QSpinBox()
        self.top_k_input.setRange(1, 500)
        self.top_k_input.setValue(50)
        self.top_k_input.setFixedWidth(70)

        controls_layout.addWidget(topk_label)
        controls_layout.addWidget(self.top_k_input)
        # tool button para sort
        self.sort_button = ToolButton("🐔", "Ordenar sprites por tamanho", self.sort_sprites)
        controls_layout.addWidget(self.sort_button)

        # Adiciona o layout horizontal ao layout principal
        self.layout.addLayout(controls_layout)

        self.tag_display = None
        self.proceed_button = None

        self._build()

    def _build(self):
        self.loading_widget = LoadingScreen("\U0001F9E0 Carregando sprites e tags...")
        self.layout.addWidget(self.loading_widget)

        self.worker = self.app_service.worker.get_worker(self._load_data)
        self.worker.finished.connect(self._on_data_loaded)
        self.worker.start()

    def _load_data(self):
        try:
            self.manager.load_all()
            return "OK"
        except Exception as e:
            return e

    def _on_data_loaded(self, result):
        self.layout.removeWidget(self.loading_widget)
        self.loading_widget.setParent(None)
        self.layout.addWidget(self.back_button)

        if isinstance(result, Exception):
            error_box = StringListBox([f"[ERRO] Falha ao carregar dados: {result}"])
            self.layout.addWidget(error_box)
            return

        tag_type_options = [("Exibir todos os sprites", -1)] + [
            (tt.name, tt.id) for tt in self.manager.get_all_tag_types()
        ]
        self.tag_type_dropdown.set_items(tag_type_options)

        all_tags_options = [("Nenhuma tag selecionada", -1)] + self.manager.get_tag_dropdown_options()
        self.filter_dropdown.set_items(all_tags_options)
        self.assist_dropdown.set_items(all_tags_options)

        self._update_sprite_grid(self.manager.get_all_sprites())
        self.layout.addWidget(self.grid)

    def _on_tag_type_selected(self):
        tag_type_id = self.tag_type_dropdown.get_selected_id()

        for comp in [self.tag_display, self.proceed_button]:
            if comp:
                self.layout.removeWidget(comp)
                comp.setParent(None)

        self.tag_display = None
        self.proceed_button = None

        tag_type = next((tt for tt in self.manager.get_all_tag_types() if tt.id == tag_type_id), None)
        if tag_type is None:
            return

        sprites = self.manager.get_unlabeled_sprites(tag_type_id)
        print("Sprites size: " + str(len(sprites)))
        tags = self.manager.get_tags_by_tag_type(tag_type_id)

        self.tag_display = TagDisplay(
            tag_type=tag_type,
            tags=tags,
            on_add_tag_callback=self._on_create_tag
        )
        self.layout.addWidget(self.tag_display)

        self.proceed_button = CustomButton("\U0001F4E4 Prosseguir", self._on_proceed)
        self.layout.addWidget(self.proceed_button)
        self._update_sprite_grid(sprites)

    def _on_filter_tag_selected(self):
        tag_type_id = self.tag_type_dropdown.get_selected_id()
        self.current_sprites = self.manager.get_unlabeled_sprites(tag_type_id)

        tag_id = self.filter_dropdown.get_selected_id()
        if tag_id == -1:
            self._update_sprite_grid(self.current_sprites)
            return

        tag = self.manager.get_tag_by_id(tag_id)
        if not tag:
            return

        # IDs dos sprites já exibidos no grid
        current_ids = {s.id for s in self.current_sprites}

        # Sprites da tag selecionada
        filtered = [s for s in tag.sprites if s.id in current_ids]
        self._update_sprite_grid(filtered)

    def _on_assist_tag_selected(self):
        tag_id = self.assist_dropdown.get_selected_id()
        tag_type_id = self.tag_type_dropdown.get_selected_id()
        if tag_id == -1 or tag_type_id == -1:
            print("[Info] Nenhuma tag selecionada para curar")
            return

        tag = self.manager.get_tag_by_id(tag_id)
        if not tag:
            return

        sprites = self.current_sprites
        sprite_responses = [self.app_service.db.get_sprite_by_id(s.id) for s in sprites if s]

        top_k = self.top_k_input.value()
        curated = self.manager.get_top_k_curated_sprites_by_tag(tag.id, sprite_responses, top_k=top_k)

        self._update_sprite_grid(curated)

    def _update_sprite_grid(self, sprites_dto):
        self.current_sprites = sprites_dto
        sprite_widgets = [
            SelectableSprite(sprite_id=s.id, image_path=s.path, selection_callback=self.grid.on_selection_toggled)
            for s in sprites_dto
        ]
        self.grid.update_grid(sprite_widgets)

    def _on_proceed(self):
        if not self.tag_display:
            return

        tag_dto = self.tag_display.get_selected_tag()
        if not tag_dto:
            print("Tag não selecionada, por favor, selecione uma tag para continuar.")
            return

        tag_type = self.tag_display.tag_type
        label = f"{tag_type.name}: {tag_dto.name}"
        selected_sprites = self.grid.get_selected_infos()

        self.update_confirm_screen(tag_dto.id, label, selected_sprites)
        self.navi("confirm")

    def _open_create_tag_type_popup(self):
        popup = CreateTagTypePopup(self._create_tag_type)
        popup.exec()

    def _create_tag_type(self, name: str):
        self.manager.create_tag_type(name)
        tag_type_options = [("<Selecionar tipo de tag>", -1)] + [
            (tt.name, tt.id) for tt in self.manager.get_all_tag_types()
        ]
        self.tag_type_dropdown.set_items(tag_type_options)

    def _on_create_tag(self, tag_type_dto, _ignored_name=None):
        popup = CreateTagPopup(lambda name, description: self._create_tag(tag_type_dto, name, description))
        popup.exec()

    def _create_tag(self, tag_type_dto, tag_name: str, description: str):
        self.manager.create_tag(tag_type_dto.id, tag_name, description)
        if self.tag_display:
            updated_tags = self.manager.get_tags_by_tag_type(tag_type_dto.id)
            self.tag_display.update_tags(updated_tags)

        all_tags_options = [("Nenhuma tag selecionada", -1)] + self.manager.get_tag_dropdown_options()
        self.filter_dropdown.set_items(all_tags_options)
        self.assist_dropdown.set_items(all_tags_options)

    def sort_sprites(self):
        self._update_sprite_grid(self.manager.sort_sprites(self.current_sprites))

    def refresh(self):
        self.manager.load_all()
        self._on_filter_tag_selected()
