# interface/components/string_box_list.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea


class StringListBox(QWidget):
    def __init__(self, strings: list[str]):
        super().__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Título de contagem
        count_label = QLabel(f"🔢 Itens encontrados: {len(strings)}")
        count_label.setStyleSheet("font-weight: bold; padding-left: 4px;")
        layout.addWidget(count_label)

        # Scrollable area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        content = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setSpacing(5)

        for string in strings:
            label = QLabel(string)
            label.setWordWrap(True)
            label.setStyleSheet("padding: 4px; background-color: #ecf0f1; border-radius: 5px;")
            content_layout.addWidget(label)

        content.setLayout(content_layout)
        scroll.setWidget(content)

        layout.addWidget(scroll)
        self.setLayout(layout)