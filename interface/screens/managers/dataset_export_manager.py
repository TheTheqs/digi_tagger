from database.db_service import DBService
from services.dataset_exporter_service import DatasetExporterService


class DatasetExportManager:
    def __init__(self, db: DBService):
        self.db = db
        self.exporter = DatasetExporterService(self.db)

    def export_dataset(self) -> str:
        try:
            self.exporter.export()
            return "[SUCESSO] Dataset exportado com sucesso para 'data/dataset/'!"
        except Exception as e:
            return f"[ERRO] Falha na exportação do dataset: {str(e)}"
