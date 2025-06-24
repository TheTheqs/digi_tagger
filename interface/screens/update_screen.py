# interface/screens/update_database_screen.py

from PySide6.QtWidgets import QWidget, QVBoxLayout
from interface.components.title import Title
from interface.components.back_button import BackButton
from interface.components.loading_screen import LoadingScreen
from interface.components.string_list_box import StringListBox

class UpdateDatabaseScreen(QWidget):
    def __init__(self, navigate_callback, app_service):
        super().__init__()

        self.navi = navigate_callback
        self.app_service = app_service
        self.worker = None
        self.loading_widget = LoadingScreen("⏳ Atualizando Banco de Dados...")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.title = Title("🔄 Atualização de Sprites")
        self.layout.addWidget(self.title)

        self.back_button = BackButton(lambda: self.navi("home"))

        self.result_widget = None

    def start_update(self, directory_path: str):
        self._clear_result_widget()

        self.layout.addWidget(self.loading_widget)

        # Cria o worker via factory
        self.worker = self.app_service.worker.get_worker(self.update, directory_path)
        self.worker.finished.connect(self._on_update_finished)
        self.worker.start()

    def update(self, directory_path: str) -> list[str]:
        logs = []
        paths = self.app_service.map.map_directory(directory_path)

        for path in paths:
            sprite = self.app_service.db.create_sprite(path)
            if sprite:
                logs.append(f"[SUCESSO] Novo Sprite: {path}")
            else:
                logs.append(f"[ERRO] Falha ao registrar: {path}")

        return logs

    def _on_update_finished(self, result):
        self.layout.removeWidget(self.loading_widget)
        self.loading_widget.setParent(None)

        self.layout.addWidget(self.back_button)

        if isinstance(result, Exception):
            logs = [f"[FATAL ERROR] {result}"]
        else:
            logs = result

        self.result_widget = StringListBox(logs)
        self.layout.addWidget(self.result_widget)

    def _clear_result_widget(self):
        if self.result_widget:
            self.layout.removeWidget(self.result_widget)
            self.result_widget.setParent(None)
            self.result_widget = None

        self.layout.removeWidget(self.back_button)
        self.back_button.setParent(None)
