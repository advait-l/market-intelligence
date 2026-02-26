from __future__ import annotations

from fastapi import APIRouter

from app.db.client import get_supabase_client
from app.db.models import OHLC_TABLE, STOCKS_TABLE
from app.schemas.responses import StockInfo, StocksResponse

router = APIRouter()


@router.get("/stocks", response_model=StocksResponse)
async def list_stocks() -> StocksResponse:
    """Return all tickers that have ingested OHLC data, along with their min/max date range."""
    supabase = get_supabase_client()

    # Fetch all stocks
    stocks_result = supabase.table(STOCKS_TABLE).select("id,ticker").execute()
    if not stocks_result.data:
        return StocksResponse(stocks=[])

    stock_map = {row["id"]: row["ticker"] for row in stocks_result.data}

    # For each stock, get min and max date from ohlc_daily
    infos: list[StockInfo] = []
    for stock_id, ticker in stock_map.items():
        ohlc_result = (
            supabase.table(OHLC_TABLE)
            .select("date")
            .eq("stock_id", stock_id)
            .order("date", desc=False)
            .limit(1)
            .execute()
        )
        if not ohlc_result.data:
            continue  # skip stocks with no OHLC rows

        min_date = ohlc_result.data[0]["date"]

        ohlc_max_result = (
            supabase.table(OHLC_TABLE)
            .select("date")
            .eq("stock_id", stock_id)
            .order("date", desc=True)
            .limit(1)
            .execute()
        )
        max_date = ohlc_max_result.data[0]["date"]

        infos.append(StockInfo(ticker=ticker, min_date=min_date, max_date=max_date))

    # Sort alphabetically by ticker
    infos.sort(key=lambda s: s.ticker)

    return StocksResponse(stocks=infos)
