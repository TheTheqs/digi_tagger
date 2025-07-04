# interface/screens/managers/update_database_manager.py

from typing import List
from database.dtos import SpriteRequestDTO
from database.db_service import DBService
from services.map_service import MapService
from services.sizer_service import SizerService
from services.embedder_service import EmbedderService


class UpdateDatabaseManager:
    def __init__(self, db: DBService, mapper: MapService, sizer: SizerService, embedder: EmbedderService):
        self.db = db
        self.mapper = mapper
        self.sizer = sizer
        self.embedder = embedder

    def update_sprites_from_directory(self, directory_path: str) -> List[str]:
        logs = []

        # Etapa 1: mapear imagens
        paths = self.mapper.map_directory(directory_path)
        if not paths:
            logs.append(f"[INFO] Nenhum arquivo encontrado em {directory_path}")
            return logs

        # Etapa 2: processar e registrar cada sprite
        for path in paths:
            try:
                vector = self.embedder.get_serialized_embedding(path)
                size = self.sizer.calculate_size(path)
                dto = SpriteRequestDTO(path=path, vector=vector, size=size)

                self.db.create_sprite(dto)
                logs.append(f"[SUCESSO] Sprite registrado com sucesso: {path}")
            except Exception as e:
                logs.append(f"[ERRO] Falha ao processar '{path}': {str(e)}")

        return logs
