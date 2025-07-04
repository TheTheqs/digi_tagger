# interface/screens/confirm_sprites_screen.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QMessageBox

from interface.components.back_button import BackButton
from interface.components.sprite_grid import SpriteGrid
from interface.components.selectable_sprite import SelectableSprite
from interface.components.custom_button import CustomButton
from services.application_services import ApplicationService
from interface.screens.managers.confirm_sprites_manager import ConfirmSpritesManager
from database.dtos import SpriteResumeDTO


class ConfirmSpritesScreen(QWidget):
    def __init__(self, navigate_callback, app_service: ApplicationService):
        super().__init__()

        self.navi = navigate_callback
        self.app_service = app_service
        self.manager = ConfirmSpritesManager(app_service.db)

        # Layout principal
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Botão de voltar
        self.back_button = BackButton(lambda: self.navi("home"))
        self.layout.addWidget(self.back_button)

        # Título
        self.title_label = QLabel("🔍 Confirmação de Sprites")
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.layout.addWidget(self.title_label)

        # Info da tag selecionada
        self.tag_info_label = QLabel("")
        self.tag_info_label.setStyleSheet("font-size: 18px; margin-bottom: 12px;")
        self.layout.addWidget(self.tag_info_label)

        # Grid de sprites
        self.sprite_grid = SpriteGrid(sprites_per_row=10)
        self.layout.addWidget(self.sprite_grid)

        # Botões de ação
        self.delete_button = CustomButton("❌ Remover Selecionados", self._on_delete_selected)
        self.save_button = CustomButton("✅ Salvar", self._on_save)

        self.layout.addWidget(self.delete_button)
        self.layout.addWidget(self.save_button)

    def set_context(self, tag_id: int, tag_name: str, sprites: list[tuple[int, str]]):
        """
        Chamada pública para montar a tela com dados recebidos da tela anterior.
        `sprites` vem como lista de tuplas (id, path), então convertemos para DTO.
        """
        dto_list = [SpriteResumeDTO(id=sid, path=path) for sid, path in sprites]
        self.manager.set_context(tag_id, tag_name, dto_list)

        self.tag_info_label.setText(f"Tag selecionada: {tag_name}")
        self._update_grid()

    def _update_grid(self):
        sprite_dtos = self.manager.get_all_sprites()
        sprite_widgets = [
            SelectableSprite(
                sprite_id=s.id,
                image_path=s.path,
                selection_callback=self.sprite_grid.on_selection_toggled
            )
            for s in sprite_dtos
        ]
        self.sprite_grid.update_grid(sprite_widgets)

    def _on_delete_selected(self):
        selected_ids = self.sprite_grid.get_selected_ids()
        if not selected_ids:
            QMessageBox.information(self, "Nada Selecionado", "Nenhum sprite selecionado para remoção.")
            return

        self.manager.remove_sprites_by_ids(selected_ids)
        self._update_grid()

    def _on_save(self):
        try:
            self.manager.save()
            QMessageBox.information(self, "Sucesso", "Tags associadas com sucesso!")
            self.navi("tagging")  # volta para a tela anterior
        except Exception as e:
            QMessageBox.critical(self, "Erro ao salvar", str(e))
