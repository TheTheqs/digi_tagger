from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QMessageBox

from interface.components.back_button import BackButton
from interface.components.sprite_grid import SpriteGrid
from interface.components.selectable_sprite import SelectableSprite
from interface.components.custom_button import CustomButton


class ConfirmSpritesScreen(QWidget):
    def __init__(self, navigate_callback, app_service):
        super().__init__()

        self.navi = navigate_callback
        self.app_service = app_service

        # Estado atual da tela
        self.current_tag_id = None
        self.current_tag_name = ""
        self.current_sprites = []

        # Componentes
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.back_button = BackButton(lambda: self.navi("home"))
        self.layout.addWidget(self.back_button)

        self.title_label = QLabel("🔍 Confirmação de Sprites")
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.layout.addWidget(self.title_label)

        self.tag_info_label = QLabel("")  # mostra tag type + tag name
        self.tag_info_label.setStyleSheet("font-size: 18px; margin-bottom: 12px;")
        self.layout.addWidget(self.tag_info_label)

        self.sprite_grid = SpriteGrid(sprites_per_row=10)
        self.layout.addWidget(self.sprite_grid)

        # Botões inferiores
        self.delete_button = CustomButton("❌ Remover Selecionados", self._on_delete_selected)
        self.save_button = CustomButton("✅ Salvar", self._on_save)

        self.layout.addWidget(self.delete_button)
        self.layout.addWidget(self.save_button)

    def update_grid(self, tag_id: int, tag_name: str, sprite_tuples: list[tuple[int, str]]):
        """Atualiza a tela com novos dados"""
        self.current_tag_id = tag_id
        self.current_tag_name = tag_name
        self.current_sprites = sprite_tuples

        self.tag_info_label.setText(f"Tag selecionada: {tag_name}")
        self._update_grid()

    def _update_grid(self):
        sprite_widgets = [
            SelectableSprite(
                sprite_id=sid,
                image_path=path,
                selection_callback=self.sprite_grid.on_selection_toggled
            )
            for sid, path in self.current_sprites
        ]
        self.sprite_grid.update_grid(sprite_widgets)

    def _on_delete_selected(self):
        selected_ids = self.sprite_grid.get_selected_ids()
        if not selected_ids:
            QMessageBox.information(self, "Nada Selecionado", "Nenhum sprite selecionado para remoção.")
            return

        # Atualiza a lista mantendo apenas os que não foram selecionados
        self.current_sprites = [t for t in self.current_sprites if t[0] not in selected_ids]
        self._update_grid()

    def _on_save(self):
        if not self.current_sprites or self.current_tag_id is None:
            QMessageBox.warning(self, "Erro", "Nenhum sprite ou tag válida.")
            return

        for sprite_id, _ in self.current_sprites:
            self.app_service.db.add_tag_to_sprite(sprite_id, self.current_tag_id)

        QMessageBox.information(self, "Sucesso", "Tags associadas com sucesso!")
        self.navi("tagging")  # Volta pra tela anterior
