from PySide6.QtWidgets import QMainWindow, QStackedWidget

from interface.screens.confirm_sprites_screen import ConfirmSpritesScreen
from interface.screens.dataset_export_screen import DatasetExportScreen
from interface.screens.home_screen import HomeScreen
from interface.screens.review_screen import ReviewScreen
from interface.screens.tagging_grid_screen import TaggingGridScreen
from interface.screens.update_screen import UpdateDatabaseScreen
from services.application_services import ApplicationService
from utils.data_printer import DataPrinter


class MainWindow(QMainWindow):
    def __init__(self, app_service: ApplicationService):
        super().__init__()
        self.app_service = app_service
        self.setWindowTitle("DigiTagger")
        self.setMinimumSize(500, 200)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        #Screens
        self.home_screen = HomeScreen(self.navigate)
        self.update_screen = UpdateDatabaseScreen(self.navigate, self.app_service)
        self.tagging_screen = TaggingGridScreen(self.navigate, self.app_service, self.update_confirm_screen)
        self.review_screen = ReviewScreen(self.navigate, self.app_service)
        self.confirm_screen = ConfirmSpritesScreen(self.navigate, self.app_service)
        self.export_screen = DatasetExportScreen(self.navigate, self.app_service)

        self.stack.addWidget(self.home_screen)
        self.stack.addWidget(self.update_screen)
        self.stack.addWidget(self.tagging_screen)
        self.stack.addWidget(self.review_screen)
        self.stack.addWidget(self.confirm_screen)
        self.stack.addWidget(self.export_screen)

        # Home Screen
        self.stack.setCurrentWidget(self.home_screen)

    def navigate(self, destiny: str):
        if destiny == "home":
            self.stack.setCurrentWidget(self.home_screen)
        elif destiny == "update":
            self.update_screen.start_update("/home/paulo/matheqs/downloads/sprites/edited")
            self.stack.setCurrentWidget(self.update_screen)
        elif destiny == "data":
            DataPrinter(self.app_service.db).print_data()
        elif destiny == "tagging":
            self.tagging_screen.refresh()
            self.stack.setCurrentWidget(self.tagging_screen)
        elif destiny == "review":
            self.review_screen.refresh()
            self.stack.setCurrentWidget(self.review_screen)
        elif destiny == "confirm":
            self.stack.setCurrentWidget(self.confirm_screen)
        elif destiny == "export":
            self.export_screen.start_export()
            self.stack.setCurrentWidget(self.export_screen)

    def update_confirm_screen(self, tag_id: int, tag_name: str, sprite_tuples: list[tuple[int, str]]):
        self.confirm_screen.set_context(tag_id, tag_name, sprite_tuples)