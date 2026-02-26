import json
import os
from datetime import date

import requests
import streamlit as st


st.set_page_config(page_title="AI Equity Research Agent", layout="wide")

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Space Grotesk', sans-serif;
    }
    .stApp {
        background: radial-gradient(circle at 10% 20%, #f2f4f8 0%, #faf7f2 45%, #eef3f8 100%);
    }
    .hero {
        padding: 1.5rem 1.2rem;
        border-radius: 18px;
        background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(245,247,250,0.85));
        box-shadow: 0 18px 40px rgba(20, 30, 55, 0.08);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>AI Equity Research Agent</h1>
        <p>Select stocks, compute technical signals, and generate a thesis with Gemini.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(ttl=60)
def fetch_stocks() -> list[dict]:
    """Fetch available stocks with their date ranges from the backend."""
    try:
        response = requests.get(f"{BACKEND_URL}/stocks", timeout=10)
        response.raise_for_status()
        return response.json().get("stocks", [])
    except Exception:
        return []


stocks = fetch_stocks()

if not stocks:
    st.warning(
        "No ingested stocks found. Please ingest stock data via the backend before running analysis."
    )
    st.stop()

# Build lookup: ticker -> {min_date, max_date}
stock_map: dict[str, dict] = {s["ticker"]: s for s in stocks}
ticker_options = sorted(stock_map.keys())

st.subheader("Run Analysis")

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    selected_tickers = st.multiselect(
        "Stocks",
        options=ticker_options,
        placeholder="Select one or more tickers...",
    )

# Compute date range intersection for all selected tickers
if selected_tickers:
    min_date = max(date.fromisoformat(stock_map[t]["min_date"]) for t in selected_tickers)
    max_date = min(date.fromisoformat(stock_map[t]["max_date"]) for t in selected_tickers)
    # Clamp: if intersection is invalid (no overlap), fall back to union
    if min_date > max_date:
        min_date = min(date.fromisoformat(stock_map[t]["min_date"]) for t in selected_tickers)
        max_date = max(date.fromisoformat(stock_map[t]["max_date"]) for t in selected_tickers)
else:
    min_date = date.today()
    max_date = date.today()

with col2:
    start_date = st.date_input("Start date", value=min_date, key="start_date")
with col3:
    end_date = st.date_input("End date", value=max_date, key="end_date")

if st.button("Analyze", disabled=not selected_tickers):
    payload = {
        "tickers": selected_tickers,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
    }
    with st.spinner("Running analysis..."):
        response = requests.post(
            f"{BACKEND_URL}/analyze",
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"},
            timeout=180,
        )
    if response.ok:
        data = response.json()
        for result in data.get("results", []):
            st.markdown(f"### {result['ticker']}")
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("RSI", f"{result['indicators'].get('rsi', 0):.2f}")
            col_b.metric("MACD", f"{result['indicators'].get('macd', 0):.2f}")
            col_c.metric("Signal", result["indicators"].get("signal", "neutral"))
            st.write(result["thesis"])
    else:
        st.error(f"Analysis failed: {response.text}")
