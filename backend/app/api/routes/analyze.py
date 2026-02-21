from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter

from app.agents.graph import run_graph
from app.schemas.requests import AnalyzeRequest
from app.schemas.responses import AnalyzeResponse, AnalysisResult


router = APIRouter()


def extract_ticker(ticker_str: str) -> str:
    """Extract ticker from string, removing _EOD suffix if present"""
    stem = Path(ticker_str).stem
    if stem.endswith("_EOD"):
        return stem[:-4]
    return stem


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    results = []
    for ticker in request.tickers:
        clean_ticker = extract_ticker(ticker)
        state = run_graph(
            {
                "ticker": clean_ticker,
                "start_date": request.start_date,
                "end_date": request.end_date,
            }
        )

        results.append(
            AnalysisResult(
                ticker=clean_ticker,
                date_range={"start": request.start_date, "end": request.end_date},
                indicators=state.get("indicators", {}),
                thesis=state.get("final_report", ""),
                analysis_id=state.get("analysis_id", ""),
            )
        )

    return AnalyzeResponse(results=results)
