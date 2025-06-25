from PySide6.QtWidgets import QMainWindow, QStackedWidget

from interface.screens.data_screen import DataScreen
from interface.screens.edit_sprite_screen import EditSpriteScreen
from interface.screens.home_screen import HomeScreen
from interface.screens.review_screen import ReviewScreen
from interface.screens.tag_admin_screen import TagAdminScreen
from interface.screens.update_screen import UpdateDatabaseScreen
from services.application_services import ApplicationService


class MainWindow(QMainWindow):
    def __init__(self, app_service: ApplicationService):
        super().__init__()
        self.app_service = app_service
        self.setWindowTitle("DigiScrap")
        self.setMinimumSize(500, 200)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        #Screens
        self.home_screen = HomeScreen(self.navigate)
        self.tag_admin_screen = TagAdminScreen(self.navigate, app_service)
        self.data_screen = DataScreen(self.navigate, app_service)
        self.update_screen = UpdateDatabaseScreen(self.navigate, self.app_service)
        self.edit_sprite_screen = EditSpriteScreen(self.navigate, self.app_service)
        self.review_screen = ReviewScreen(self.navigate, self.app_service)

        self.stack.addWidget(self.home_screen)
        self.stack.addWidget(self.tag_admin_screen)
        self.stack.addWidget(self.data_screen)
        self.stack.addWidget(self.update_screen)
        self.stack.addWidget(self.edit_sprite_screen)
        self.stack.addWidget(self.review_screen)

        # Home Screen
        self.stack.setCurrentWidget(self.home_screen)

    def navigate(self, destiny: str):
        if destiny == "home":
            self.stack.setCurrentWidget(self.home_screen)
        elif destiny == "update":
            self.update_screen.start_update("/home/paulo/matheqs/downloads/sprites/raw")
            self.stack.setCurrentWidget(self.update_screen)
        elif destiny == "data":
            self.data_screen.update_screen()
            self.stack.setCurrentWidget(self.data_screen)
        elif destiny == "edit":
            self.edit_sprite_screen.load_next_sprite()
            self.stack.setCurrentWidget(self.edit_sprite_screen)
        elif destiny == "tags":
            self.stack.setCurrentWidget(self.tag_admin_screen)
        elif destiny == "review":
            self.stack.setCurrentWidget(self.review_screen)