from PIL import Image

class SizerService:
    def __init__(self):
        pass  # pode ter dependências no futuro

    def calculate_size(self, path: str) -> int:
        with Image.open(path).convert("RGBA") as img:
            width, height = img.size
            pixels = img.load()

            active_pixels = 0
            for y in range(height):
                for x in range(width):
                    r, g, b, a = pixels[x, y]
                    if a > 0 and (r > 10 or g > 10 or b > 10):
                        active_pixels += 1

            return active_pixels