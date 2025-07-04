# utils/tag_initializer.py

from database.db_service import DBService
from database.dtos import TagTypeRequestDTO, TagRequestDTO

class TagInitializer:
    def __init__(self, db: DBService):
        self.db = db

    def run_if_empty(self):
        print("[INFO] Iniciando processo base de população do banco...")
        self._create_tag_types()
        self._create_tags()
        print("[INFO] Banco populado com sucesso!")

    def _create_tag_types(self):
        if self.db.get_all_tag_types():
            print("[INFO] Tag Types já existem, iniciando criação de tags.")
            for tag_type in self.db.get_all_tag_types():
                if tag_type.name == "main_color":
                    self.main_color_type = tag_type
                elif tag_type.name == "size":
                    self.size_type = tag_type
                elif tag_type.name == "body_shape":
                    self.body_shape = tag_type
        print("[INFO] Tag Types não encontradas, iniciando criação das entidades.")
        self.main_color_type = self.db.create_tag_type(TagTypeRequestDTO("main_color"))
        self.size_type = self.db.create_tag_type(TagTypeRequestDTO("size"))
        self.body_shape = self.db.create_tag_type(TagTypeRequestDTO("body_shape"))
        print(f"[TYPE][+] Criado TagType: main_color (ID: {self.main_color_type.id})")
        print(f"[TYPE][+] Criado TagType: size (ID: {self.size_type.id})")
        print(f"[TYPE][+] Criado TagType: body_shape (ID: {self.body_shape.id})")

    def _create_tags(self):
        if self.db.get_all_tags():
            print("[INFO] Tags já existem, o banco de dados já possui população base.")
            return
        print("[INFO] Tags não encontradas, iniciando população base do banco.")
        self._create_main_color_tags()
        self._create_size_tags()
        self._create_body_shape_tags()

    def _create_main_color_tags(self):
        colors = {
            "white": "The most prominent color is white.",
            "black": "The most prominent color is black.",
            "gray": "The most prominent color is gray.",
            "yellow": "The most prominent color is yellow.",
            "red": "The most prominent color is red.",
            "blue": "The most prominent color is blue.",
            "green": "The most prominent color is green.",
            "brown": "The most prominent color is brown."
        }

        for name, desc in colors.items():
            self.db.create_tag(TagRequestDTO(self.main_color_type.id, name, desc))
            print(f"[TAG][+] Criada tag: main_color:{name}")

    def _create_size_tags(self):
        descriptions = {
            "I": "A very small creature in the center of the image.",
            "II": "A medium-sized creature with space around it.",
            "III": "A very large creature that fills almost the entire image."
        }

        for name, desc in descriptions.items():
            self.db.create_tag(TagRequestDTO(self.size_type.id, name, desc))
            print(f"[TAG][+] Criada tag: size:{name}")

    def _create_body_shape_tags(self):
        shapes = {
            "round": "A round-bodied creature with no limbs.",
            "humanoid": "A biped human-like creature",
            "sturdy": "A bulky, strong creature",
            "quadruped": "A four-legged and quadruped creature",
            "insectoid": "A bug-like creature.",
            "chibi": "A chibi creature with cute face and tiny limbs",
        }

        for name, desc in shapes.items():
            self.db.create_tag(TagRequestDTO(self.body_shape.id, name, desc))
            print(f"[TAG][+] Criada tag: body_shape:{name}")