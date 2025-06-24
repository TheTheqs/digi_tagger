from database.db_service import DbService
from database.engine import init_db
import sys
from PySide6.QtWidgets import QApplication

from interface.main_window import MainWindow
from services.application_services import ApplicationService
from services.map_service import MapService
from services.worker_service import WorkerService


def main():
    print("Inicializando o banco de dados Eyeing...")
    init_db()
    print("Banco de dados criado com sucesso!")
    #Instâncias
    db_service = DbService()
    worker_service = WorkerService()
    map_service = MapService()
    app_service = ApplicationService(db_service, map_service, worker_service)
    app = QApplication(sys.argv)
    window = MainWindow(app_service)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
