from PySide6.QtWidgets import QVBoxLayout, QDialog, QCheckBox
from interface.components.text_input import TextInput
from interface.components.custom_button import CustomButton

class CreateTagTypePopup(QDialog):
    def __init__(self, on_save_callback):
        super().__init__()

        self.on_save_callback = on_save_callback
        self.setWindowTitle("Criar Novo TagType")
        self.setMinimumWidth(300)

        layout = QVBoxLayout()

        # Campo de texto (nome)
        self.name_input = TextInput("Nome do TagType", "Digite o nome")
        layout.addWidget(self.name_input)

        # Checkbox (exclusive)
        self.exclusive_checkbox = QCheckBox("Exclusivo")
        layout.addWidget(self.exclusive_checkbox)

        # Botão salvar
        save_button = CustomButton("Salvar", self._save)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def _save(self):
        name = self.name_input.text().strip()
        exclusive = self.exclusive_checkbox.isChecked()

        if name:
            self.on_save_callback(name, exclusive)
            self.accept()  # Fecha o popup após salvar
        else:
            print("O nome não pode ser vazio.")
