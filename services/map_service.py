# services/map_service.py

import os
from typing import List

class MapService:
    def __init__(self):
        pass

    def map_directory(self, directory_path: str) -> List[str]:
        if not os.path.isdir(directory_path):
            print(f"[ERROR] Diretório inválido: {directory_path}")
            return []

        files = [
            os.path.join(directory_path, f)
            for f in os.listdir(directory_path)
            if os.path.isfile(os.path.join(directory_path, f)) and f.lower().endswith('.png')
        ]

        print(f"[INFO] {len(files)} arquivos .png encontrados em: {directory_path}")
        return files
