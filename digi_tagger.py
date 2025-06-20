from database.db_service import DbService
from database.engine import init_db
import sys
from PySide6.QtWidgets import QApplication

from interface.main_window import MainWindow
from services.application_services import ApplicationService


def main():
    print("Inicializando o banco de dados Eyeing...")
    init_db()
    print("Banco de dados criado com sucesso!")
    #Instâncias
    db_service = DbService()
    app_service = ApplicationService(db_service)
    app = QApplication(sys.argv)
    window = MainWindow(app_service)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
