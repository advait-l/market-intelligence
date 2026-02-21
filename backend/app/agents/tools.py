from __future__ import annotations

from typing import Any, Dict, List

import pandas as pd

from app.db.models import ANALYSES_TABLE, EMBEDDINGS_TABLE, OHLC_TABLE, STOCKS_TABLE
from app.services.embeddings import embed_text


def fetch_stock_id(supabase, ticker: str) -> str | None:
    result = supabase.table(STOCKS_TABLE).select("id").eq("ticker", ticker).execute()
    if not result.data:
        return None
    return result.data[0]["id"]


def fetch_ohlc(
    supabase,
    stock_id: str,
    start_date: str,
    end_date: str,
) -> pd.DataFrame:
    result = (
        supabase.table(OHLC_TABLE)
        .select("date,open,high,low,close,volume")
        .eq("stock_id", stock_id)
        .gte("date", start_date)
        .lte("date", end_date)
        .order("date")
        .execute()
    )
    df = pd.DataFrame(result.data)
    if not df.empty:
        df["date"] = pd.to_datetime(df["date"]).dt.date
    return df


def store_analysis(
    supabase,
    stock_id: str,
    start_date: str,
    end_date: str,
    rsi: float,
    macd: float,
    signal: str,
    summary: str,
) -> Dict[str, Any]:
    inserted = (
        supabase.table(ANALYSES_TABLE)
        .insert(
            {
                "stock_id": stock_id,
                "date_range_start": start_date,
                "date_range_end": end_date,
                "rsi": rsi,
                "macd": macd,
                "signal": signal,
                "summary": summary,
            }
        )
        .execute()
    )
    analysis = inserted.data[0]
    return analysis


def store_embedding(pg_conn, analysis_id: str, summary: str) -> List[float]:
    embedding = embed_text(summary)
    with pg_conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO analysis_embeddings (analysis_id, embedding, model) VALUES (%s, %s, %s)",
            (analysis_id, embedding, "gemini"),
        )
    pg_conn.commit()
    return embedding
