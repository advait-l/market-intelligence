from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Query

from app.db.client import get_supabase_client
from app.db.models import ANALYSES_TABLE, OHLC_TABLE, STOCKS_TABLE
from app.schemas.responses import (
    AnalysisHistory,
    AnalysisHistoryResponse,
    OhlcData,
    OhlcDataResponse,
    StockInfo,
    StocksResponse,
)

router = APIRouter()


@router.get("/analyses", response_model=AnalysisHistoryResponse)
async def get_analyses(
    ticker: str = Query(..., description="Stock ticker"),
) -> AnalysisHistoryResponse:
    supabase = get_supabase_client()

    stock_result = supabase.table(STOCKS_TABLE).select("id").eq("ticker", ticker).execute()
    if not stock_result.data:
        return AnalysisHistoryResponse(analyses=[])

    stock_id = stock_result.data[0]["id"]

    analyses_result = (
        supabase.table(ANALYSES_TABLE)
        .select("id, date_range_start, date_range_end, rsi, macd, signal, summary, created_at")
        .eq("stock_id", stock_id)
        .order("created_at", desc=True)
        .execute()
    )

    analyses = [
        AnalysisHistory(
            id=row["id"],
            date_range_start=row["date_range_start"],
            date_range_end=row["date_range_end"],
            rsi=row["rsi"],
            macd=row["macd"],
            signal=row["signal"],
            summary=row["summary"],
            created_at=row["created_at"],
        )
        for row in (analyses_result.data or [])
    ]

    return AnalysisHistoryResponse(analyses=analyses)


@router.get("/ohlc", response_model=OhlcDataResponse)
async def get_ohlc(
    ticker: str = Query(..., description="Stock ticker"),
    start_date: str | None = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: str | None = Query(None, description="End date (YYYY-MM-DD)"),
) -> OhlcDataResponse:
    supabase = get_supabase_client()

    stock_result = supabase.table(STOCKS_TABLE).select("id").eq("ticker", ticker).execute()
    if not stock_result.data:
        return OhlcDataResponse(ticker=ticker, data=[])

    stock_id = stock_result.data[0]["id"]

    query = (
        supabase.table(OHLC_TABLE)
        .select("date,open,high,low,close,volume")
        .eq("stock_id", stock_id)
    )

    if start_date:
        query = query.gte("date", start_date)
    if end_date:
        query = query.lte("date", end_date)

    ohlc_result = query.order("date").execute()

    data = [
        OhlcData(
            date=row["date"],
            open=row["open"],
            high=row["high"],
            low=row["low"],
            close=row["close"],
            volume=row["volume"],
        )
        for row in (ohlc_result.data or [])
    ]

    return OhlcDataResponse(ticker=ticker, data=data)


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
