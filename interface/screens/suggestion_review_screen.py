# interface/screens/suggestion_review_screen.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QMessageBox

from interface.components.title import Title
from interface.components.back_button import BackButton
from interface.components.custom_button import CustomButton
from interface.components.tag_display import TagDisplay
from interface.components.dropdown import Dropdown
from interface.components.sprite_grid import SpriteGrid
from interface.components.selectable_sprite import SelectableSprite
from interface.components.create_tag_popup import CreateTagPopup
from interface.components.create_tag_type_popup import CreateTagTypePopup
from services.application_services import ApplicationService


class SuggestionReviewScreen(QWidget):
    def __init__(self, navigate_callback, app_service: ApplicationService):
        super().__init__()

        self.navi = navigate_callback
        self.app_service = app_service
        self.current_sprite_tuples = []  # (id, path)
        self.suggestion_id = None  # Atual suggestion
        self.tag_display = None

        # Layout base
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.title = Title("🔍 Revisão de Sugestão IA")
        self.layout.addWidget(self.title)

        self.back_button = BackButton(lambda: self.navi("home"))
        self.layout.addWidget(self.back_button)

        # Info de Suggestion
        self.suggestion_info_label = QLabel("")
        self.layout.addWidget(self.suggestion_info_label)

        # Dropdown de TagType
        self.create_tag_type_button = CustomButton("Criar TagType", self._open_create_tag_type_popup)
        self.layout.addWidget(self.create_tag_type_button)

        self.tag_type_dropdown = Dropdown(self._get_tag_type_options())
        self.tag_type_dropdown.currentIndexChanged.connect(self._on_tag_type_selected)
        self.layout.addWidget(self.tag_type_dropdown)

        # Grid de sprites
        self.sprite_grid = SpriteGrid(sprites_per_row=10)
        self.layout.addWidget(self.sprite_grid)

        # Botões de ação
        self.remove_button = CustomButton("❌ Remover Selecionados", self._on_remove_selected)
        self.confirm_button = CustomButton("✅ Confirmar Sugestão", self._on_confirm_suggestion)
        self.layout.addWidget(self.remove_button)
        self.layout.addWidget(self.confirm_button)

        # Carregar sugestão inicial
        self._load_next_suggestion()

    def _get_tag_type_options(self) -> list[tuple[str, int]]:
        tag_types = self.app_service.db.get_all_tag_types()
        return [("<Nenhum TagType selecionado>", -1)] + tag_types

    def _open_create_tag_type_popup(self):
        popup = CreateTagTypePopup(self._create_tag_type)
        popup.exec()

    def _create_tag_type(self, name: str):
        self.app_service.db.create_tag_type(name)
        self.tag_type_dropdown.set_items(self._get_tag_type_options())

    def _on_tag_type_selected(self):
        # Remove tag_display antigo se houver
        if self.tag_display:
            self.layout.removeWidget(self.tag_display)
            self.tag_display.setParent(None)
            self.tag_display = None

        tag_type_id = self.tag_type_dropdown.get_selected_id()
        if tag_type_id == -1:
            return

        tag_type_name = self.tag_type_dropdown.get_selected_text()
        tag_options = self.app_service.db.get_tags_by_tag_type(tag_type_id)

        self.tag_display = TagDisplay(
            tag_type_id=tag_type_id,
            tag_type_name=tag_type_name,
            tag_items=tag_options,
            on_add_tag_callback=self._on_create_tag
        )
        self.layout.insertWidget(6, self.tag_display)  # abaixo do dropdown

        # Filtra sprites que já têm uma tag desse tipo
        valid_sprites = []
        ignored_count = 0
        for sprite_id, path in self.current_sprite_tuples:
            if not self.app_service.db.sprite_has_tag_type(sprite_id, tag_type_id):
                valid_sprites.append((sprite_id, path))
            else:
                ignored_count += 1

        self.current_sprite_tuples = valid_sprites
        self._update_grid()

        if ignored_count > 0:
            QMessageBox.information(
                self,
                "Sprites ignorados",
                f"{ignored_count} sprite(s) foram ignorados porque já possuem uma tag do tipo '{tag_type_name}'."
            )

    def _on_create_tag(self, tag_type_id: int, tag_type_name: str):
        popup = CreateTagPopup(lambda name: self._create_tag(tag_type_id, tag_type_name, name))
        popup.exec()

    def _create_tag(self, tag_type_id: int, tag_type_name: str, tag_name: str):
        self.app_service.db.create_tag(tag_name=tag_name, tag_type_id=tag_type_id)
        if self.tag_display:
            updated_tags = self.app_service.db.get_tags_by_tag_type(tag_type_id)
            self.tag_display.update_tags(updated_tags)

    def call_next(self):
        self._load_next_suggestion()

    def _load_next_suggestion(self):
        total = self.app_service.db.get_total_suggestions_count()
        suggestion = self.app_service.db.get_next_unverified_suggestion()
        if suggestion is None:
            if total > 0:
                QMessageBox.information(self, "Tudo revisado!",
                                        f"Não há mais sugestões pendentes.\nSugestões totais: {total}")

            return

        self.suggestion_id = suggestion.suggestion_id
        self.suggestion_info_label.setText(f"Suggestion ID: {self.suggestion_id} — Total: {total}")

        # Aqui carregamos os paths, mas vamos buscar os IDs correspondentes
        sprite_tuples = self.app_service.db.get_sprite_id_by_paths(suggestion.sprite_paths)
        self.current_sprite_tuples = sprite_tuples

        self._update_grid()

    def _update_grid(self):
        sprite_widgets = [
            SelectableSprite(sprite_id=sid, image_path=path, selection_callback=self.sprite_grid.on_selection_toggled)
            for sid, path in self.current_sprite_tuples
        ]
        self.sprite_grid.update_grid(sprite_widgets)

    def _on_remove_selected(self):
        selected_ids = self.sprite_grid.get_selected_ids()
        self.current_sprite_tuples = [t for t in self.current_sprite_tuples if t[0] not in selected_ids]
        self._update_grid()

    def _on_confirm_suggestion(self):
        if not self.tag_display:
            QMessageBox.warning(self, "TagType não selecionado", "Escolha uma TagType para continuar.")
            return

        tag = self.tag_display.get_selected_tag()
        if not tag:
            QMessageBox.warning(self, "Tag não selecionada", "Escolha uma Tag para prosseguir.")
            return

        tag_id, _ = tag

        if not self.current_sprite_tuples:
            QMessageBox.information(self, "Nada para taggear",
                                    "Todos os sprites desta sugestão já possuem tag do tipo selecionado.")
            return

        for sprite_id, _ in self.current_sprite_tuples:
            self.app_service.db.add_tag_to_sprite(sprite_id, tag_id)

        self.app_service.db.mark_suggestion_as_verified(self.suggestion_id)
        QMessageBox.information(self, "Concluído", "Sugestão marcada como verificada e sprites taggeados com sucesso!")
        self._load_next_suggestion()
