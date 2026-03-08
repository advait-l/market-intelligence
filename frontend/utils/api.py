import json
import os
from typing import Any

import requests
import streamlit as st

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

PING_REQUEST_TIMEOUT = 20
PING_INTERVAL_SECS = 3
PING_ATTEMPT_LIMIT = 10


@st.cache_data(ttl=60)
def fetch_stocks() -> list[dict[str, Any]]:
    try:
        response = requests.get(f"{BACKEND_URL}/stocks", timeout=10)
        response.raise_for_status()
        return response.json().get("stocks", [])
    except Exception:
        return []


@st.cache_data(ttl=30)
def fetch_analyses(ticker: str) -> list[dict[str, Any]]:
    try:
        response = requests.get(f"{BACKEND_URL}/analyses", params={"ticker": ticker}, timeout=10)
        response.raise_for_status()
        return response.json().get("analyses", [])
    except Exception:
        return []


@st.cache_data(ttl=60)
def fetch_ohlc(
    ticker: str, start_date: str | None = None, end_date: str | None = None
) -> dict[str, Any]:
    try:
        params: dict[str, str] = {"ticker": ticker}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        response = requests.get(f"{BACKEND_URL}/ohlc", params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception:
        return {"ticker": ticker, "data": []}


def ping_backend() -> bool:
    try:
        resp = requests.get(f"{BACKEND_URL}/ping", timeout=PING_REQUEST_TIMEOUT)
        resp.raise_for_status()
        return True
    except Exception:
        return False


def run_analysis(ticker: str, start_date: str, end_date: str) -> dict[str, Any]:
    payload = {
        "tickers": [ticker],
        "start_date": start_date,
        "end_date": end_date,
    }
    response = requests.post(
        f"{BACKEND_URL}/analyze",
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"},
        timeout=180,
    )
    response.raise_for_status()
    return response.json()
