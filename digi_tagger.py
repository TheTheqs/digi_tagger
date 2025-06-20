from database.engine import init_db
import sys
from PySide6.QtWidgets import QApplication

from interface.main_window import MainWindow


def main():
    print("Inicializando o banco de dados Eyeing...")
    init_db()
    print("Banco de dados criado com sucesso!")

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
