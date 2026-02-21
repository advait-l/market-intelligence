from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    tickers: List[str] = Field(..., min_length=1)
    start_date: str
    end_date: str
