# services/worker_service.py

from services.worker.worker_thread import WorkerThread

class WorkerService:
    def __init__(self):
        pass  # Nada de estado, apenas fábrica

    def get_worker(self, func, *args, **kwargs) -> WorkerThread:
        return WorkerThread(func, *args, **kwargs)
