from database.db_service import DBService
from database.engine import init_db
import sys
from PySide6.QtWidgets import QApplication
from interface.main_window import MainWindow
from services.application_services import ApplicationService
from services.map_service import MapService
from services.strategies.clustering.topk_similarity_clustering import TopKSimilarityClusteringStrategy
from services.strategies.embeddings.clip_strategy import CLIPEmbeddingStrategy
from services.suggestion_generator_service import SuggestionGeneratorService
from services.worker_service import WorkerService


def main():
    print("Inicializando o banco de dados...")
    init_db()
    print("Banco de dados iniciado com sucesso!")

    #Estratégias
    cluster = TopKSimilarityClusteringStrategy(top_k=50, max_suggestions=1024)
    clip_strategy = CLIPEmbeddingStrategy(device="cpu")

    #Instâncias
    db_service = DBService()
    worker_service = WorkerService()
    map_service = MapService()
    suggestor = SuggestionGeneratorService(
        clip_strategy,
        cluster
    )
    app_service = ApplicationService(db_service, map_service, worker_service, suggestor)
    app = QApplication(sys.argv)
    #  app_service.db.make_edited_sprite_usable()
    window = MainWindow(app_service)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
