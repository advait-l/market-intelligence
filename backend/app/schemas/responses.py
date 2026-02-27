from __future__ import annotations

from typing import Dict, List

from pydantic import BaseModel


class AnalysisResult(BaseModel):
    ticker: str
    date_range: Dict[str, str]
    indicators: Dict[str, float | str]
    thesis: str
    analysis_id: str


class AnalyzeResponse(BaseModel):
    results: List[AnalysisResult]


class IngestResponse(BaseModel):
    ticker: str
    rows: int


class StockInfo(BaseModel):
    ticker: str
    min_date: str
    max_date: str


class StocksResponse(BaseModel):
    stocks: List[StockInfo]


class AnalysisHistory(BaseModel):
    id: str
    date_range_start: str
    date_range_end: str
    rsi: float
    macd: float
    signal: str
    summary: str
    created_at: str


class AnalysisHistoryResponse(BaseModel):
    analyses: List[AnalysisHistory]


class OhlcData(BaseModel):
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int


class OhlcDataResponse(BaseModel):
    ticker: str
    data: List[OhlcData]
