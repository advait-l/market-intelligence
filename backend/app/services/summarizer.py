from __future__ import annotations

import google.generativeai as genai

from app.core.config import settings


def generate_text(prompt: str) -> str:
    genai.configure(api_key=settings.gemini_api_key)
    model = genai.GenerativeModel(settings.gemini_model)
    response = model.generate_content(prompt)
    return response.text or ""
