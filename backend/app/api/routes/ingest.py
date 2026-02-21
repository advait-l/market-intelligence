from __future__ import annotations

from pathlib import Path
from typing import List

from fastapi import APIRouter, File, UploadFile

from app.db.client import get_supabase_client
from app.ingestion.csv_parser import parse_csv_bytes
from app.ingestion.loader import load_ohlc_data
from app.schemas.responses import IngestResponse
from app.utils.filehash import hash_bytes


router = APIRouter()


def extract_ticker(filename: str) -> str:
    stem = Path(filename).stem
    if stem.endswith("_EOD"):
        return stem[:-4]
    return stem


@router.post("/ingest", response_model=List[IngestResponse])
async def ingest_csv(files: List[UploadFile] = File(...)):
    supabase = get_supabase_client()
    responses: List[IngestResponse] = []

    for file in files:
        content = await file.read()
        filename_ticker = extract_ticker(file.filename or "")
        df = parse_csv_bytes(content, ticker=filename_ticker)

        # Use ticker from CSV if available, otherwise use filename
        if "ticker" in df.columns:
            ticker = df["ticker"].iloc[0]
            df = df.drop(columns=["ticker"])
        else:
            ticker = filename_ticker

        source_hash = hash_bytes(content)
        result = load_ohlc_data(supabase, ticker, df, source_hash)
        responses.append(IngestResponse(ticker=ticker, rows=result["rows"]))

    return responses
