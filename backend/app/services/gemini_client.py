from __future__ import annotations

import logging
import time
from typing import List

import google.api_core.exceptions
import google.generativeai as genai

from app.core.config import settings

logger = logging.getLogger(__name__)

_configured = False


def _configure():
    global _configured
    if not _configured:
        genai.configure(api_key=settings.gemini_api_key)
        _configured = True


def _is_rate_limit_error(e: Exception) -> bool:
    if isinstance(e, google.api_core.exceptions.ResourceExhausted):
        return True
    if hasattr(e, "code") and e.code == 429:
        return True
    if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
        return True
    return False


def _exponential_backoff(attempt: int) -> float:
    return settings.gemini_retry_base_delay * (2**attempt)


def generate_text(prompt: str) -> str:
    _configure()

    last_exception = None
    models = settings.gemini_text_models

    for model_idx, model_name in enumerate(models):
        if model_idx > 0:
            logger.info(f"Falling back to model: {model_name}")

        for attempt in range(settings.gemini_max_retries):
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                return response.text or ""
            except Exception as e:
                last_exception = e
                if _is_rate_limit_error(e):
                    if attempt < settings.gemini_max_retries - 1:
                        delay = _exponential_backoff(attempt)
                        logger.warning(
                            f"Rate limited on {model_name}, attempt {attempt + 1}, "
                            f"retrying in {delay}s: {e}"
                        )
                        time.sleep(delay)
                    else:
                        logger.warning(
                            f"Rate limited on {model_name}, exhausted retries, trying next model"
                        )
                        break
                else:
                    raise

    raise last_exception or RuntimeError("All models exhausted")


def embed_text(text: str) -> List[float]:
    _configure()

    last_exception = None
    models = settings.gemini_embedding_models

    for model_idx, model_name in enumerate(models):
        if model_idx > 0:
            logger.info(f"Falling back to embedding model: {model_name}")

        for attempt in range(settings.gemini_max_retries):
            try:
                response = genai.embed_content(
                    model=model_name,
                    content=text,
                )
                embedding = getattr(response, "embedding", None)
                if embedding is None:
                    embedding = response["embedding"]
                return embedding
            except Exception as e:
                last_exception = e
                if _is_rate_limit_error(e):
                    if attempt < settings.gemini_max_retries - 1:
                        delay = _exponential_backoff(attempt)
                        logger.warning(
                            f"Rate limited on {model_name}, attempt {attempt + 1}, "
                            f"retrying in {delay}s: {e}"
                        )
                        time.sleep(delay)
                    else:
                        logger.warning(
                            f"Rate limited on {model_name}, exhausted retries, trying next model"
                        )
                        break
                else:
                    raise

    raise last_exception or RuntimeError("All embedding models exhausted")
