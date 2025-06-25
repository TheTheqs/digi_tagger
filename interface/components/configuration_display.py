# interface/components/configuration_display.py

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame

class ConfigurationDisplay(QWidget):
    def __init__(self, configuration_data: list[tuple[str, str]]):
        """
        configuration_data: lista de tuplas (tag_type_name, tag_name)
        """
        super().__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)

        for tag_type_name, tag_name in configuration_data:
            row = QHBoxLayout()
            print(tag_type_name + ": " + tag_name)
            key_label = QLabel(f'"{tag_type_name}":')
            key_label.setStyleSheet("font-weight: bold; font-family: monospace;")
            row.addWidget(key_label)

            value_label = QLabel(f'"{tag_name}"')
            value_label.setStyleSheet("font-family: monospace; color: #555555;")
            row.addWidget(value_label)

            row.addStretch()
            layout.addLayout(row)

            # linha divisória opcional entre chaves:
            line = QFrame()
            line.setFrameShape(QFrame.Shape.HLine)
            line.setStyleSheet("color: #DDDDDD;")
            layout.addWidget(line)

        self.setLayout(layout)
