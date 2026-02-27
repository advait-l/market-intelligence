from __future__ import annotations

from app.services.gemini_client import generate_text as _generate_text


def generate_text(prompt: str) -> str:
    return _generate_text(prompt)
