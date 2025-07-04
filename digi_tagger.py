from database.db_service import DBService
from database.engine import init_db
import sys
from PySide6.QtWidgets import QApplication
from interface.main_window import MainWindow
from services.application_services import ApplicationService
from services.assisted_curation_service import AssistedCurationService
from services.embedder_service import EmbedderService
from services.map_service import MapService
from services.sizer_service import SizerService
from services.strategies.embeddings.clip_strategy import CLIPEmbeddingStrategy
from services.worker_service import WorkerService
from utils.tag_initializer import TagInitializer
from tests.unit_test.embedding_test import deserialize_test

def tests():
    message: dict = {
        True:  "\033[92m[Sucesso]\033[0m ",  # verde
        False: "\033[91m[Falha]  \033[0m "   # vermelho
    }
    result, source = deserialize_test()
    print(f"{message[result]} {source}")

def main():
    reset_banco: bool = True
    reset_message: dict = {
        True: "\033[93m[RESET]\033[0m Tags antigas serão apagadas antes de inicializar.",
        False: "\033[96m[INFO]\033[0m Mantendo tags existentes. Nenhuma exclusão será feita."
    }
    print("Inicializando o banco de dados...")
    init_db()
    print("Banco de dados iniciado com sucesso!")

    #Estratégias
    clip_strategy: CLIPEmbeddingStrategy = CLIPEmbeddingStrategy()

    #Instâncias
    db_service = DBService()
    worker_service = WorkerService()
    map_service = MapService()
    sizer = SizerService()
    embedder = EmbedderService(clip_strategy)
    assist = AssistedCurationService(clip_strategy)
    app_service = ApplicationService(db_service, map_service, worker_service, sizer, embedder, assist)
    app = QApplication(sys.argv)
    print(reset_message[reset_banco])
    if reset_banco:
        db_service.delete_all_tags()
        db_service.delete_all_tag_types()
    TagInitializer(db_service).run_if_empty()
    tests()

    # Inicialização da janela
    window = MainWindow(app_service)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
