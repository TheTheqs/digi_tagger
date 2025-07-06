from database.db_service import DBService

class AutoSizer:
    def __init__(self, db: DBService):
        self.db = db

    def auto_size(self):
        sprites = self.db.get_all_sprites()
        total = len(sprites)
        base = total // 5
        remainder = total % 5  # o que sobra após divisão exata

        # Distribui a sobra nos primeiros blocos
        sizes = [base + (1 if i < remainder else 0) for i in range(5)]

        # Cria os cortes baseados nos tamanhos
        cuts = []
        start = 0
        for size in sizes:
            cuts.append(sprites[start:start + size])
            start += size

        tag_type = self.db.get_tag_type_by_name("batch")
        tags = self.db.get_tags_by_tag_type(tag_type.id)

        for i in range(5):
            for sprite in cuts[i]:
                self.db.add_tag_to_sprite(sprite.id, tags[i].id)
