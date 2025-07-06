# services/strategies/embeddings/clip_strategy.py

import torch
import clip
import numpy as np
from PIL import Image
import io
import os

from services.strategies.embeddings.base import EmbeddingStrategy


class CLIPEmbeddingStrategy(EmbeddingStrategy):
    def __init__(self, device: str = None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)

    def get_serialized_embedding(self, image_path: str) -> bytes:
        embedding = self._get_embedding(image_path)
        return self._serialize_embedding(embedding)

    def get_raw_embedding(self, image_path: str) -> np.ndarray:
        return self._get_embedding(image_path)

    def _get_embedding(self, image_path: str) -> np.ndarray:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Imagem não encontrada: {image_path}")

        image = Image.open(image_path).convert("RGB")

        # Redimensionamento fiel (pixel-perfect) 96x96 → 192x192
        upscale_factor = 3
        resized_image = image.resize(
            (image.width * upscale_factor, image.height * upscale_factor),
            resample=Image.Resampling.NEAREST
        )

        image_input = self.preprocess(resized_image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            image_features = self.model.encode_image(image_input)
            image_features /= image_features.norm(dim=-1, keepdim=True)

        return image_features.cpu().numpy().flatten()

    def get_text_embedding(self, text: str) -> np.ndarray:
        text_tokens = clip.tokenize([text]).to(self.device)

        with torch.no_grad():
            text_features = self.model.encode_text(text_tokens)
            text_features /= text_features.norm(dim=-1, keepdim=True)

        return text_features.cpu().numpy().flatten()

    def _serialize_embedding(self, embedding: np.ndarray) -> bytes:
        """
        Serializa um vetor de embedding usando np.save com dtype e shape forçados.
        """

        embedding = embedding.astype(np.float32).flatten()

        if embedding.shape[0] != 512:
            raise ValueError(f"[ERRO] Embedding com shape inválido: {embedding.shape}, esperado (512,)")

        buffer: io.BytesIO = io.BytesIO()
        np.save(buffer, embedding, allow_pickle=False)
        data = buffer.getvalue()

        print(f"[DEBUG] Serializado: {len(data)} bytes | dtype={embedding.dtype} | shape={embedding.shape}")
        return data