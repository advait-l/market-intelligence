import json
import os
import time
from datetime import date, timedelta

import requests
import streamlit as st


st.set_page_config(page_title="AI Equity Research Agent", layout="wide")

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# How long to wait for the backend to wake up before giving up.
WAKE_TIMEOUT_SECS = 90
PING_INTERVAL_SECS = 3
PING_ATTEMPT_LIMIT = WAKE_TIMEOUT_SECS // PING_INTERVAL_SECS

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
    .wake-box {
        padding: 2rem 1.5rem;
        border-radius: 14px;
        background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(240,244,255,0.85));
        box-shadow: 0 8px 24px rgba(20, 30, 55, 0.07);
        text-align: center;
        margin-top: 2rem;
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

# ---------------------------------------------------------------------------
# Phase 1: Wake-up polling
# ---------------------------------------------------------------------------
# Track whether the backend is confirmed alive across reruns.
if "backend_ready" not in st.session_state:
    st.session_state.backend_ready = False
if "ping_attempts" not in st.session_state:
    st.session_state.ping_attempts = 0

if not st.session_state.backend_ready:
    attempts = st.session_state.ping_attempts

    if attempts >= PING_ATTEMPT_LIMIT:
        st.error(
            "The backend service did not respond in time. "
            "Please refresh the page in a moment to try again."
        )
        st.stop()

    wake_placeholder = st.empty()
    wake_placeholder.markdown(
        f"""
        <div class="wake-box">
            <h3>Starting up the backend service...</h3>
            <p>Free-tier services sleep when idle. This usually takes 30–60 seconds.</p>
            <p style="color:#888; font-size:0.85rem;">Attempt {attempts + 1} of {PING_ATTEMPT_LIMIT}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.spinner("Waiting for backend to come online..."):
        try:
            resp = requests.get(f"{BACKEND_URL}/ping", timeout=PING_INTERVAL_SECS)
            resp.raise_for_status()
            st.session_state.backend_ready = True
            st.session_state.ping_attempts = 0
            wake_placeholder.empty()
        except Exception:
            st.session_state.ping_attempts += 1
            time.sleep(PING_INTERVAL_SECS)

    st.rerun()

# ---------------------------------------------------------------------------
# Phase 2: Load available stocks
# ---------------------------------------------------------------------------


@st.cache_data(ttl=60)
def fetch_stocks() -> list[dict]:
    """Fetch available stocks with their date ranges from the backend."""
    try:
        response = requests.get(f"{BACKEND_URL}/stocks", timeout=10)
        response.raise_for_status()
        return response.json().get("stocks", [])
    except Exception:
        return []


with st.spinner("Loading available stocks..."):
    stocks = fetch_stocks()

if not stocks:
    st.warning(
        "No ingested stocks found. Please ingest stock data via the backend before running analysis."
    )
    st.stop()

# ---------------------------------------------------------------------------
# Phase 3: Analysis UI
# ---------------------------------------------------------------------------

# Build lookup: ticker -> {min_date, max_date}
stock_map: dict[str, dict] = {s["ticker"]: s for s in stocks}
ticker_options = sorted(stock_map.keys())

st.subheader("Run Analysis")

col1, col2 = st.columns([2, 3])

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

# Period selector
PERIODS: dict[str, timedelta | None] = {
    "Last 7 days": timedelta(days=7),
    "Last 1 month": timedelta(days=30),
    "Last 3 months": timedelta(days=90),
    "Last 6 months": timedelta(days=180),
    "Custom": None,
}

with col2:
    selected_period = st.radio(
        "Period",
        options=list(PERIODS.keys()),
        index=2,  # default: Last 3 months
        horizontal=True,
        key="period",
    )

# Resolve start / end dates
end_date = max_date
if selected_period == "Custom":
    cust_col1, cust_col2 = st.columns(2)
    with cust_col1:
        start_date = st.date_input(
            "Start date",
            value=min_date,
            min_value=min_date,
            max_value=max_date,
            key="custom_start",
        )
    with cust_col2:
        end_date = st.date_input(
            "End date",
            value=max_date,
            min_value=min_date,
            max_value=max_date,
            key="custom_end",
        )
else:
    offset: timedelta = PERIODS[selected_period]  # type: ignore[assignment]
    start_date = max(min_date, max_date - offset)

# Always show the resolved range so the user knows what will be submitted
st.caption(f"Date range: **{start_date.isoformat()}** to **{end_date.isoformat()}**")

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
