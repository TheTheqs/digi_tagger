from PySide6.QtWidgets import QWidget, QVBoxLayout
from interface.components.title import Title
from interface.components.back_button import BackButton
from interface.components.loading_screen import LoadingScreen
from interface.components.string_list_box import StringListBox
from interface.screens.managers.dataset_export_manager import DatasetExportManager
from services.application_services import ApplicationService


class DatasetExportScreen(QWidget):
    def __init__(self, navigate_callback, app_service: ApplicationService):
        super().__init__()

        self.navi = navigate_callback
        self.app_service: ApplicationService = app_service
        self.manager = DatasetExportManager(db=app_service.db)

        self.worker = None
        self.result_widget = None
        self.loading_widget = LoadingScreen("📦 Exportando Dataset para Treinamento...")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.title = Title("📁 Exportação de Dataset")
        self.layout.addWidget(self.title)

        self.back_button = BackButton(lambda: self.navi("home"))

    def start_export(self):
        self._clear_result_widget()
        self.layout.addWidget(self.loading_widget)

        self.worker = self.app_service.worker.get_worker(self.manager.export_dataset)
        self.worker.finished.connect(self._on_export_finished)
        self.worker.start()

    def _on_export_finished(self, result: str):
        self.layout.removeWidget(self.loading_widget)
        self.loading_widget.setParent(None)

        self.layout.addWidget(self.back_button)

        self.result_widget = StringListBox([result])
        self.layout.addWidget(self.result_widget)

    def _clear_result_widget(self):
        if self.result_widget:
            self.layout.removeWidget(self.result_widget)
            self.result_widget.setParent(None)
            self.result_widget = None

        self.layout.removeWidget(self.back_button)
        self.back_button.setParent(None)
