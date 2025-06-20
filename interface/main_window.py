from PySide6.QtWidgets import QMainWindow, QStackedWidget
from interface.screens.home_screen import HomeScreen
from interface.screens.tag_admin_screen import TagAdminScreen
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

        self.stack.addWidget(self.home_screen)
        self.stack.addWidget(self.tag_admin_screen)

        # Home Screen
        self.stack.setCurrentWidget(self.home_screen)

    def navigate(self, destiny: str):
        if destiny == "home":
            self.stack.setCurrentWidget(self.home_screen)
        elif destiny == "update":
            print("Entrando em update...")
        elif destiny == "analyse":
            print("Entrando em analyse...")
        elif destiny == "edit":
            print("Entrando em edit...")
        elif destiny == "tags":
            self.stack.setCurrentWidget(self.tag_admin_screen)