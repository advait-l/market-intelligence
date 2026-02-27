from __future__ import annotations

from typing import List

from app.services.gemini_client import embed_text as _embed_text


def embed_text(text: str) -> List[float]:
    return _embed_text(text)
