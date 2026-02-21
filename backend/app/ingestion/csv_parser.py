from __future__ import annotations

from io import BytesIO
from typing import Dict, Optional

import pandas as pd

from app.ingestion.validator import REQUIRED_COLUMNS, validate_ohlc_df, has_ticker_column


def parse_csv_bytes(content: bytes, ticker: Optional[str] = None) -> pd.DataFrame:
    df = pd.read_csv(BytesIO(content))
    result = validate_ohlc_df(df)
    if not result.ok:
        raise ValueError("; ".join(result.errors))

    rename_map: Dict[str, str] = {}
    for original, normalized in result.normalized_columns.items():
        if normalized in REQUIRED_COLUMNS:
            rename_map[original] = REQUIRED_COLUMNS[normalized]

    df = df.rename(columns=rename_map)

    # Check if ticker column exists in CSV
    if has_ticker_column(df):
        # Extract ticker from CSV if not provided
        if ticker is None and "ticker" in df.columns:
            ticker = df["ticker"].iloc[0]
        df = df.drop(columns=["ticker"], errors="ignore")

    df = df[list(REQUIRED_COLUMNS.values())]
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
    df = df.dropna(subset=["date"]).reset_index(drop=True)
    return df
