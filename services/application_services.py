from database.db_service import DBService
from services.assisted_curation_service import AssistedCurationService
from services.embedder_service import EmbedderService
from services.map_service import MapService
from services.sizer_service import SizerService
from services.worker_service import WorkerService


class ApplicationService:
    def __init__(self,
                 db_service: DBService,
                 map_service: MapService,
                 worker_service: WorkerService,
                 sizer_service: SizerService,
                 embedder_service: EmbedderService,
                 assist: AssistedCurationService
                 ):
        self.db = db_service
        self.map = map_service
        self.worker = worker_service
        self.sizer = sizer_service
        self.embedder = embedder_service
        self.assist = assist
