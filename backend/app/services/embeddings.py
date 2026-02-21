from __future__ import annotations

from typing import List

import google.generativeai as genai

from app.core.config import settings


def embed_text(text: str) -> List[float]:
    genai.configure(api_key=settings.gemini_api_key)
    response = genai.embed_content(
        model=settings.gemini_embedding_model,
        content=text,
    )
    embedding = getattr(response, "embedding", None)
    if embedding is None:
        embedding = response["embedding"]
    return embedding
