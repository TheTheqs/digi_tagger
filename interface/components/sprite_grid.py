# interface/components/sprite_grid.py

from PySide6.QtWidgets import QWidget, QScrollArea, QVBoxLayout, QGridLayout, QLabel
from PySide6.QtCore import Qt
from interface.components.selectable_sprite import SelectableSprite


class SpriteGrid(QWidget):
    def __init__(self, sprites_per_row: int = 10, show_info: bool = True):
        super().__init__()
        self._sprites_per_row = sprites_per_row
        self._sprites = []
        self._sprite_size = 120
        self._show_info = show_info


        # Label com contadores
        self._info_label = QLabel("")
        self._info_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self._info_label.setVisible(self._show_info)

        # Grid interno
        self._grid_widget = QWidget()
        self._grid_layout = QGridLayout(self._grid_widget)
        self._grid_layout.setSpacing(4)
        self._grid_layout.setContentsMargins(4, 4, 4, 4)

        self._scroll_area = QScrollArea()
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setWidget(self._grid_widget)

        # Layout principal
        main_layout = QVBoxLayout()
        if self._show_info:
            main_layout.addWidget(self._info_label)
        main_layout.addWidget(self._scroll_area)
        self.setLayout(main_layout)

    def update_grid(self, sprite_list: list[SelectableSprite]):
        while self._grid_layout.count():
            item = self._grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

        self._sprites = sprite_list

        for index, sprite in enumerate(sprite_list):
            row = index // self._sprites_per_row
            col = index % self._sprites_per_row

            sprite.setMinimumSize(self._sprite_size, self._sprite_size)
            sprite.setMaximumSize(self._sprite_size, self._sprite_size)

            # força cada sprite a saber quem é o pai (opcional, pro on_selection_toggled funcionar)
            sprite.setParent(self._grid_widget)
            self._grid_layout.addWidget(sprite, row, col)

        total_width = self._sprites_per_row * (self._sprite_size + self._grid_layout.spacing())
        self._grid_widget.setMinimumWidth(total_width)

        self._update_info_label()

    def _update_info_label(self):
        if not self._show_info:
            return
        total = len(self._sprites)
        selected = len([s for s in self._sprites if s.is_selected()])
        self._info_label.setText(f"Selecionados: {selected} / {total}")

    def on_selection_toggled(self):
        # chamada pelos filhos quando o estado muda
        self._update_info_label()

    def get_selected_ids(self) -> list[int]:
        return [sprite.get_sprite_id() for sprite in self._sprites if sprite.is_selected()]

    def get_selected_infos(self) -> list[tuple[int, str]]:
        return [sprite.get_sprite_info() for sprite in self._sprites if sprite.is_selected()]

    def set_sprites_per_row(self, value: int):
        self._sprites_per_row = max(1, value)
        self.update_grid(self._sprites)

    def set_show_info(self, value: bool):
        self._show_info = value
        self._info_label.setVisible(value)
