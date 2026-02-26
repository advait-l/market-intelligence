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
