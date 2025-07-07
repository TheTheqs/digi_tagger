# interface/screens/tagging_grid_screen.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from interface.components.title import Title
from interface.components.back_button import BackButton
from interface.components.loading_screen import LoadingScreen
from interface.components.sprite_grid import SpriteGrid
from interface.components.selectable_sprite import SelectableSprite
from interface.components.custom_button import CustomButton
from interface.components.dropdown import Dropdown
from interface.components.string_list_box import StringListBox
from interface.screens.managers.review_manager import ReviewManager
from services.application_services import ApplicationService


class ReviewScreen(QWidget):
    def __init__(self, navigate_callback, app_service: ApplicationService):
        super().__init__()

        self.navi = navigate_callback
        self.app_service = app_service
        self.manager: ReviewManager = ReviewManager(app_service.db)
        self.current_sprites = []
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.selected_sprites: list[int] = []
        self.selected_tag: int = -1
        self.title = Title("\U0001F9E9 Review de Sprites")
        self.layout.addWidget(self.title)

        self.back_button = BackButton(lambda: self.navi("home"))
        self.grid = SpriteGrid(sprites_per_row=10)

        self.remove_tag_button = CustomButton("Remover Tags", self._on_remove_tags)
        self.layout.addWidget(self.remove_tag_button)

        # Layout horizontal para os controles superiores
        controls_layout = QHBoxLayout()

        # Dropdown – Filtro geral
        self.filter_dropdown = Dropdown([("\U0001F50E Filtrar por tag (qualquer tipo)", -1)])
        self.filter_dropdown.setMinimumWidth(200)
        self.filter_dropdown.currentIndexChanged.connect(self._on_filter_tag_selected)
        controls_layout.addWidget(self.filter_dropdown)

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

        all_tags_options = [("Nenhuma tag selecionada", -1)] + self.manager.get_tag_dropdown_options()
        self.filter_dropdown.set_items(all_tags_options)

        self._update_sprite_grid(self.manager.get_all_sprites())
        self.layout.addWidget(self.grid)

    def _on_filter_tag_selected(self):
        self.current_sprites = self.manager.get_all_sprites()

        tag_id = self.filter_dropdown.get_selected_id()
        if tag_id == -1:
            self._update_sprite_grid(self.current_sprites)
            return

        tag = self.manager.get_tag_by_id(tag_id)
        if not tag:
            return

        # IDs dos sprites carregados
        current_ids = {s.id for s in self.current_sprites}

        # Sprites da tag selecionada
        filtered = [s for s in tag.sprites if s.id in current_ids]
        self._update_sprite_grid(filtered)

    def _update_sprite_grid(self, sprites_dto):
        self.current_sprites = sprites_dto
        sprite_widgets = [
            SelectableSprite(sprite_id=s.id, image_path=s.path, selection_callback=self.grid.on_selection_toggled)
            for s in sprites_dto
        ]
        self.grid.update_grid(sprite_widgets)

    def _on_remove_tags(self):
        self.selected_sprites = self.grid.get_selected_ids()
        self.selected_tag = self.filter_dropdown.get_selected_id()
        self.manager.remove_tag(self.selected_sprites, self.selected_tag)
        self._on_filter_tag_selected()

    def refresh(self):
        self.manager.load_all()
        all_tags_options = [("Nenhuma tag selecionada", -1)] + self.manager.get_tag_dropdown_options()
        self.filter_dropdown.set_items(all_tags_options)