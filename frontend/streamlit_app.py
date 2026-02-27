import json
import os
import time
from datetime import date, timedelta

import plotly.graph_objects as go
import requests
import streamlit as st


st.set_page_config(page_title="AI Equity Research Agent", layout="wide")

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

WAKE_TIMEOUT_SECS = 90
PING_INTERVAL_SECS = 3
PING_ATTEMPT_LIMIT = WAKE_TIMEOUT_SECS // PING_INTERVAL_SECS

st.markdown(
    """
    <style>
    .sidebar-title {
        padding: 1rem 0;
    }
    .wake-box {
        padding: 2rem 1.5rem;
        border-radius: 14px;
        text-align: center;
        margin-top: 2rem;
    }
    .analysis-card {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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
            <p>Attempt {attempts + 1} of {PING_ATTEMPT_LIMIT}</p>
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


@st.cache_data(ttl=60)
def fetch_stocks() -> list[dict]:
    try:
        response = requests.get(f"{BACKEND_URL}/stocks", timeout=10)
        response.raise_for_status()
        return response.json().get("stocks", [])
    except Exception:
        return []


@st.cache_data(ttl=30)
def fetch_analyses(ticker: str) -> list[dict]:
    try:
        response = requests.get(f"{BACKEND_URL}/analyses", params={"ticker": ticker}, timeout=10)
        response.raise_for_status()
        return response.json().get("analyses", [])
    except Exception:
        return []


@st.cache_data(ttl=60)
def fetch_ohlc(ticker: str, start_date: str | None = None, end_date: str | None = None) -> dict:
    try:
        params = {"ticker": ticker}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        response = requests.get(f"{BACKEND_URL}/ohlc", params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception:
        return {"ticker": ticker, "data": []}


with st.spinner("Loading available stocks..."):
    stocks = fetch_stocks()

if not stocks:
    st.warning(
        "No ingested stocks found. Please ingest stock data via the backend before running analysis."
    )
    st.stop()

stock_map: dict[str, dict] = {s["ticker"]: s for s in stocks}
ticker_options = sorted(stock_map.keys())

with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-title">
            <h1>AI Equity Research Agent</h1>
            <p>Select stocks, compute technical signals, and generate a thesis with Gemini.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()
    st.subheader("Ingested Stocks")

    if "selected_stock" not in st.session_state:
        st.session_state.selected_stock = ticker_options[0] if ticker_options else None

    selected_ticker = st.radio(
        "Select a stock",
        options=ticker_options,
        index=ticker_options.index(st.session_state.selected_stock)
        if st.session_state.selected_stock in ticker_options
        else 0,
        label_visibility="collapsed",
    )
    st.session_state.selected_stock = selected_ticker

    stock_info = stock_map.get(selected_ticker, {})
    if stock_info:
        st.caption(
            f"Data range: **{stock_info.get('min_date')}** to **{stock_info.get('max_date')}**"
        )

    st.divider()

st.title(f"📊 {selected_ticker}")

ohlc_response = fetch_ohlc(selected_ticker)
ohlc_data = ohlc_response.get("data", [])

if ohlc_data:
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=[d["date"] for d in ohlc_data],
                open=[d["open"] for d in ohlc_data],
                high=[d["high"] for d in ohlc_data],
                low=[d["low"] for d in ohlc_data],
                close=[d["close"] for d in ohlc_data],
                name=selected_ticker,
            )
        ]
    )
    fig.update_layout(
        title=f"{selected_ticker} Historical EOD Prices",
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False,
        height=400,
        margin=dict(l=0, r=0, t=40, b=0),
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No OHLC data available for this stock.")

st.divider()

tab1, tab2 = st.tabs(["Analysis History", "Run New Analysis"])

with tab1:
    analyses = fetch_analyses(selected_ticker)

    if analyses:
        for analysis in analyses:
            with st.container():
                st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("RSI", f"{analysis.get('rsi', 0):.2f}")
                with col_b:
                    st.metric("MACD", f"{analysis.get('macd', 0):.2f}")
                with col_c:
                    signal = analysis.get("signal", "neutral")
                    st.metric("Signal", signal.upper())

                st.caption(
                    f"📅 {analysis.get('date_range_start')} to {analysis.get('date_range_end')} "
                    f"| Created: {analysis.get('created_at', '')[:19]}"
                )

                with st.expander("View Thesis"):
                    st.write(analysis.get("summary", "No summary available."))
                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("No analyses found for this stock. Run a new analysis to get started.")

with tab2:
    st.subheader("Run Analysis")

    stock_info = stock_map.get(selected_ticker, {})
    min_date = date.fromisoformat(stock_info.get("min_date", date.today().isoformat()))
    max_date = date.fromisoformat(stock_info.get("max_date", date.today().isoformat()))

    PERIODS: dict[str, timedelta | None] = {
        "Last 7 days": timedelta(days=7),
        "Last 1 month": timedelta(days=30),
        "Last 3 months": timedelta(days=90),
        "Last 6 months": timedelta(days=180),
        "Custom": None,
    }

    selected_period = st.radio(
        "Period",
        options=list(PERIODS.keys()),
        index=2,
        horizontal=True,
        key="period",
    )

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

    st.caption(f"Date range: **{start_date.isoformat()}** to **{end_date.isoformat()}**")

    if st.button("Analyze", type="primary"):
        payload = {
            "tickers": [selected_ticker],
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
                st.success("Analysis completed!")
                col_a, col_b, col_c = st.columns(3)
                col_a.metric("RSI", f"{result['indicators'].get('rsi', 0):.2f}")
                col_b.metric("MACD", f"{result['indicators'].get('macd', 0):.2f}")
                col_c.metric("Signal", result["indicators"].get("signal", "neutral"))
                st.write(result["thesis"])

            fetch_analyses.clear()
            st.rerun()
        else:
            st.error(f"Analysis failed: {response.text}")
