import csv
import shutil
from pathlib import Path
from typing import List
from database.dtos import SpriteResponseDTO
from database.db_service import DBService

EXPORT_DIR = Path("data/dataset")
SPRITES_DIR = EXPORT_DIR / "sprites"
CSV_PATH = EXPORT_DIR / "tags.csv"


class DatasetExporterService:
    def __init__(self, db_service: DBService):
        self.db_service = db_service

    def export(self):
        EXPORT_DIR.mkdir(parents=True, exist_ok=True)
        SPRITES_DIR.mkdir(parents=True, exist_ok=True)

        sprites: List[SpriteResponseDTO] = self.db_service.get_all_sprites_complete()

        with CSV_PATH.open("w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["filename", "type", "score", "main_color"])

            # tag_type ids
            score_id: int = self.db_service.get_tag_type_by_name("score").id
            type_id: int = self.db_service.get_tag_type_by_name("type").id
            color_id: int = self.db_service.get_tag_type_by_name("main_color").id

            for i, sprite in enumerate(sprites):
                filename = f"{i:04d}.png"
                dest_path = SPRITES_DIR / filename

                try:
                    shutil.copy(sprite.path, dest_path)
                except FileNotFoundError:
                    print(f"[WARN] Arquivo não encontrado: {sprite.path}")
                    continue

                tag_map = {tag.tag_type_id: tag.name for tag in sprite.tags}

                type_tag = tag_map.get(type_id, "N/A")
                score_tag = tag_map.get(score_id, "N/A")
                color_tag = tag_map.get(color_id, "N/A")

                writer.writerow([filename, type_tag, score_tag, color_tag])
                print(f"[INFO] Exportado: {filename} -> {type_tag}, {score_tag}, {color_tag}")

        print(f"\n[DONE] Exportação concluída para {len(sprites)} sprites.")
