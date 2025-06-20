from database.db_service import DbService


class ApplicationService:
    def __init__(self, db_service: DbService):
        self.db = db_service

    def get_db_service(self) -> DbService:
        return self.db
