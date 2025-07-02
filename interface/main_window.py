from PySide6.QtWidgets import QMainWindow, QStackedWidget

from interface.screens.confirm_sprites_screen import ConfirmSpritesScreen
from interface.screens.home_screen import HomeScreen
from interface.screens.suggestion_review_screen import SuggestionReviewScreen
from interface.screens.tagging_grid_screen import TaggingGridScreen
from interface.screens.update_screen import UpdateDatabaseScreen
from services.application_services import ApplicationService


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
        self.confirm_screen = ConfirmSpritesScreen(self.navigate, self.app_service)
        self.review_screen = SuggestionReviewScreen(self.navigate, self.app_service)

        self.stack.addWidget(self.home_screen)
        self.stack.addWidget(self.update_screen)
        self.stack.addWidget(self.tagging_screen)
        self.stack.addWidget(self.confirm_screen)
        self.stack.addWidget(self.review_screen)

        # Home Screen
        self.stack.setCurrentWidget(self.home_screen)

    def navigate(self, destiny: str):
        if destiny == "home":
            self.stack.setCurrentWidget(self.home_screen)
        elif destiny == "update":
            self.update_screen.start_update("/home/paulo/matheqs/downloads/sprites/edited")
            self.stack.setCurrentWidget(self.update_screen)
        elif destiny == "data":
            print("Data Screen")
        elif destiny == "tagging":
            self.tagging_screen.load_sprites()
            self.stack.setCurrentWidget(self.tagging_screen)
        elif destiny == "confirm":
            self.stack.setCurrentWidget(self.confirm_screen)
        elif destiny == "review":
            self.review_screen.call_next()
            self.stack.setCurrentWidget(self.review_screen)

    def update_confirm_screen(self, tag_id: int, tag_name: str, sprite_tuples: list[tuple[int, str]]):
        self.confirm_screen.update_grid(tag_id, tag_name, sprite_tuples)