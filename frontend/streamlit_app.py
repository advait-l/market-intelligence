import time

import streamlit as st

from components.analysis_panel import render_analysis_panel
from components.chart_panel import render_chart_panel
from components.indicators_panel import render_indicators_panel
from components.modals import (
    render_error_state,
    render_step_progress,
    render_success_result,
    render_wake_screen,
)
from components.navigation import render_top_nav
from components.stock_header import render_stock_header
from components.stock_list import render_stock_list
from styles.components import apply_all_styles
from utils.api import (
    PING_ATTEMPT_LIMIT,
    PING_INTERVAL_SECS,
    fetch_analyses,
    fetch_ohlc,
    fetch_stocks,
    ping_backend,
    run_analysis,
)

st.set_page_config(
    page_title="AI Equity Research",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(apply_all_styles(), unsafe_allow_html=True)

for key, default in [
    ("backend_ready", False),
    ("ping_attempts", 0),
    ("selected_stock", None),
    ("selected_period", "3M"),
    ("analyses_cache", {}),
]:
    if key not in st.session_state:
        st.session_state[key] = default

if not st.session_state.backend_ready:
    attempts = st.session_state.ping_attempts

    if attempts >= PING_ATTEMPT_LIMIT:
        st.error(
            "The backend service did not respond in time. "
            "Please refresh the page in a moment to try again."
        )
        st.stop()

    render_wake_screen(attempts, PING_ATTEMPT_LIMIT)

    if ping_backend():
        st.session_state.backend_ready = True
        st.session_state.ping_attempts = 0
    else:
        st.session_state.ping_attempts += 1
        time.sleep(PING_INTERVAL_SECS)

    st.rerun()

stocks = fetch_stocks()

if not stocks:
    st.markdown(
        """
        <div class="empty-state">
            <div class="empty-icon">📭</div>
            <p class="empty-title">No Stocks Found</p>
            <p class="empty-text">Ingest stock CSV data via the backend to get started.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

stock_map: dict[str, dict] = {s["ticker"]: s for s in stocks}
ticker_options = sorted(stock_map.keys())

if st.session_state.selected_stock not in ticker_options:
    st.session_state.selected_stock = ticker_options[0]

selected_ticker = render_top_nav(st.session_state.selected_stock, ticker_options)

if selected_ticker != st.session_state.selected_stock:
    st.session_state.selected_stock = selected_ticker
    st.rerun()

with st.sidebar:
    for ticker in ticker_options:
        if ticker not in st.session_state.analyses_cache:
            st.session_state.analyses_cache[ticker] = fetch_analyses(ticker)

    render_stock_list(
        ticker_options=ticker_options,
        stock_map=stock_map,
        selected_ticker=st.session_state.selected_stock,
        analyses_cache=st.session_state.analyses_cache,
    )

selected_ticker = st.session_state.selected_stock
stock_info = stock_map.get(selected_ticker, {})

if selected_ticker in st.session_state.analyses_cache:
    analyses = st.session_state.analyses_cache[selected_ticker]
else:
    analyses = fetch_analyses(selected_ticker)
    st.session_state.analyses_cache[selected_ticker] = analyses

ohlc_response = fetch_ohlc(selected_ticker)
ohlc_data = ohlc_response.get("data", [])

render_stock_header(
    ticker=selected_ticker,
    stock_info=stock_info,
    ohlc_data=ohlc_data,
    analyses=analyses,
)

st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)

main_content_cols = st.columns([0.7, 0.3])

with main_content_cols[0]:
    render_chart_panel(ohlc_data)

with main_content_cols[1]:

    def handle_run_analysis(start_date, end_date):
        pipeline_steps = [
            "Fetching OHLC data",
            "Computing indicators (RSI / MACD)",
            "Generating AI thesis with Gemini",
            "Saving results to database",
        ]

        st.markdown("<br>", unsafe_allow_html=True)
        step_placeholder = st.empty()

        with step_placeholder.container():
            render_step_progress(0, len(pipeline_steps), pipeline_steps)

        try:
            with st.spinner("Running analysis pipeline…"):
                api_response = run_analysis(
                    ticker=selected_ticker,
                    start_date=start_date.isoformat(),
                    end_date=end_date.isoformat(),
                )

            with step_placeholder.container():
                render_step_progress(len(pipeline_steps), len(pipeline_steps), pipeline_steps)

            for result in api_response.get("results", []):
                indicators = result.get("indicators", {})
                r_rsi = float(indicators.get("rsi") or 0)
                r_macd = float(indicators.get("macd") or 0)
                r_sig = (indicators.get("signal") or "neutral").lower()
                r_thesis = result.get("thesis", "No thesis generated.")

                render_success_result(
                    start_date=start_date.isoformat(),
                    end_date=end_date.isoformat(),
                    rsi=r_rsi,
                    macd=r_macd,
                    signal=r_sig,
                    thesis=r_thesis,
                )

            st.session_state.analyses_cache[selected_ticker] = fetch_analyses(selected_ticker)
            fetch_analyses.clear()

        except Exception as e:
            step_placeholder.empty()
            render_error_state(f"Analysis failed: {str(e)}")

    render_indicators_panel(
        ticker=selected_ticker,
        analyses=analyses,
        stock_info=stock_info,
        on_run_analysis=handle_run_analysis,
    )

st.markdown("<div class='analysis-section-wrapper'>", unsafe_allow_html=True)

render_analysis_panel(analyses)

st.markdown("</div>", unsafe_allow_html=True)
