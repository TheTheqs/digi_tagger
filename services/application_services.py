from database.db_service import DBService
from services.map_service import MapService
from services.worker_service import WorkerService


class ApplicationService:
    def __init__(self, db_service: DBService, map_service: MapService, worker_service: WorkerService):
        self.db = db_service
        self.map = map_service
        self.worker = worker_service
