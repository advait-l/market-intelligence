from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable

import pandas as pd


REQUIRED_COLUMNS = {
    "date": "date",
    "open": "open",
    "high": "high",
    "low": "low",
    "close": "close",
    "volume": "volume",
}

OPTIONAL_COLUMNS = {
    "ticker": "ticker",
}


@dataclass(frozen=True)
class ValidationResult:
    ok: bool
    errors: list[str]
    normalized_columns: Dict[str, str]


def _normalize_columns(columns: Iterable[str]) -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    for col in columns:
        normalized = col.strip().lower().replace(" ", "_")
        mapping[col] = normalized
    return mapping


def validate_ohlc_df(df: pd.DataFrame) -> ValidationResult:
    errors: list[str] = []
    mapping = _normalize_columns(df.columns)
    normalized = {mapping[col] for col in df.columns}

    missing = [col for col in REQUIRED_COLUMNS if col not in normalized]
    if missing:
        errors.append(f"Missing required columns: {', '.join(missing)}")

    return ValidationResult(ok=len(errors) == 0, errors=errors, normalized_columns=mapping)


def has_ticker_column(df: pd.DataFrame) -> bool:
    """Check if DataFrame has a ticker column"""
    mapping = _normalize_columns(df.columns)
    normalized = {mapping[col] for col in df.columns}
    return "ticker" in normalized
