from PySide6.QtWidgets import QMainWindow, QStackedWidget
from interface.screens.home_screen import HomeScreen

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DigiScrap")
        self.setMinimumSize(500, 200)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        #Screens
        self.home_screen = HomeScreen(self.navigate)

        self.stack.addWidget(self.home_screen)

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