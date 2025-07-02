# services/strategies/embeddings/clip_strategy.py

import torch
import clip
import numpy as np
from PIL import Image
from tqdm import tqdm
from typing import List
from services.strategies.embeddings.base import EmbeddingStrategy

class CLIPEmbeddingStrategy(EmbeddingStrategy):
    def __init__(self, model_name: str = "ViT-B/32", device: str = "cpu", batch_size: int = 128):
        self.device = device
        self.batch_size = batch_size
        self.model, self.preprocess = clip.load(model_name, device=device)

    def embed(self, image_paths: List[str]) -> np.ndarray:
        embeddings = []

        # Redimensionamento desejado (multiplo de 96 mais próximo de 224/240/288)
        target_size = 240  # múltiplo de 96 mais próximo de 224 (padrão do CLIP)

        for i in tqdm(range(0, len(image_paths), self.batch_size), desc="Gerando Embeddings com CLIP"):
            batch_paths = image_paths[i:i + self.batch_size]
            images = []

            for path in batch_paths:
                try:
                    img = Image.open(path).convert("RGB")
                    img = img.resize((target_size, target_size), Image.Resampling.NEAREST)
                    images.append(self.preprocess(img))
                except Exception as e:
                    print(f"[AVISO] Falha ao carregar imagem {path}: {e}")

            if not images:
                continue

            image_tensor = torch.stack(images).to(self.device)
            with torch.no_grad():
                batch_embeddings = self.model.encode_image(image_tensor)
                batch_embeddings = batch_embeddings.cpu().numpy()

            embeddings.append(batch_embeddings)

        # Concatena todos os batches
        return np.concatenate(embeddings, axis=0)
