from __future__ import annotations

from typing import Any, Dict

import pandas as pd

from app.db.models import OHLC_TABLE, STOCKS_TABLE


def get_or_create_stock(supabase, ticker: str) -> Dict[str, Any]:
    existing = supabase.table(STOCKS_TABLE).select("id,ticker").eq("ticker", ticker).execute()
    if existing.data:
        return existing.data[0]

    inserted = supabase.table(STOCKS_TABLE).insert({"ticker": ticker}).execute()
    return inserted.data[0]


def load_ohlc_data(
    supabase,
    ticker: str,
    df: pd.DataFrame,
    source_hash: str,
) -> Dict[str, Any]:
    stock = get_or_create_stock(supabase, ticker)
    stock_id = stock["id"]

    rows = []
    for _, row in df.iterrows():
        rows.append(
            {
                "stock_id": stock_id,
                "date": row["date"].isoformat(),
                "open": float(row["open"]),
                "high": float(row["high"]),
                "low": float(row["low"]),
                "close": float(row["close"]),
                "volume": int(row["volume"]),
                "source_file_hash": source_hash,
            }
        )

    if rows:
        supabase.table(OHLC_TABLE).upsert(rows, on_conflict="stock_id,date").execute()

    return {"stock_id": stock_id, "rows": len(rows)}
