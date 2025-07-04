# interface/components/create_tag_popup.py

from PySide6.QtWidgets import QVBoxLayout, QDialog
from interface.components.text_input import TextInput
from interface.components.custom_button import CustomButton

class CreateTagPopup(QDialog):
    def __init__(self, on_save_callback):
        super().__init__()

        self.on_save_callback = on_save_callback
        self.setWindowTitle("Criar Novo Tag")
        self.setMinimumWidth(300)

        layout = QVBoxLayout()

        # Campo de texto (nome)
        self.name_input = TextInput("Nome do Tag", "Digite o nome")
        layout.addWidget(self.name_input)

        # Campo de texto (descrição)
        self.description_input = TextInput("Descrição", "Descreva o que este tag representa")
        layout.addWidget(self.description_input)

        # Botão salvar
        save_button = CustomButton("Salvar", self._save)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def _save(self):
        name = self.name_input.text().strip()
        description = self.description_input.text().strip()

        if not name:
            print("O nome não pode ser vazio.")
            return

        if not description:
            print("A descrição não pode ser vazia.")
            return

        self.on_save_callback(name, description)
        self.accept()