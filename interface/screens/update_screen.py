# interface/screens/update_database_screen.py

from PySide6.QtWidgets import QWidget, QVBoxLayout
from interface.components.title import Title
from interface.components.back_button import BackButton
from interface.components.loading_screen import LoadingScreen
from interface.components.string_list_box import StringListBox
from interface.screens.managers.update_database_manager import UpdateDatabaseManager
from services.application_services import ApplicationService


class UpdateDatabaseScreen(QWidget):
    def __init__(self, navigate_callback, app_service: ApplicationService):
        super().__init__()

        self.navi = navigate_callback
        self.app_service: ApplicationService = app_service
        self.manager = UpdateDatabaseManager(
            db=app_service.db,
            mapper=app_service.map,
            sizer=app_service.sizer,
            embedder=app_service.embedder
        )

        self.worker = None
        self.result_widget = None
        self.loading_widget = LoadingScreen("⏳ Atualizando Banco de Dados...")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.title = Title("🔄 Atualização de Sprites")
        self.layout.addWidget(self.title)

        self.back_button = BackButton(lambda: self.navi("home"))

    def start_update(self, directory_path: str):
        self._clear_result_widget()
        self.layout.addWidget(self.loading_widget)

        self.worker = self.app_service.worker.get_worker(
            self.manager.update_sprites_from_directory,
            directory_path
        )
        self.worker.finished.connect(self._on_update_finished)
        self.worker.start()

    def _on_update_finished(self, result):
        self.layout.removeWidget(self.loading_widget)
        self.loading_widget.setParent(None)

        self.layout.addWidget(self.back_button)

        logs = result if isinstance(result, list) else [f"[FATAL ERROR] {result}"]

        self.result_widget = StringListBox(logs)
        self.layout.addWidget(self.result_widget)

    def _clear_result_widget(self):
        if self.result_widget:
            self.layout.removeWidget(self.result_widget)
            self.result_widget.setParent(None)
            self.result_widget = None

        self.layout.removeWidget(self.back_button)
        self.back_button.setParent(None)
