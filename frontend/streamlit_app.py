import json
import os
import time
from datetime import date, timedelta

import plotly.graph_objects as go
import requests
import streamlit as st
from plotly.subplots import make_subplots


st.set_page_config(
    page_title="AI Equity Research",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

WAKE_TIMEOUT_SECS = 90
PING_INTERVAL_SECS = 3
PING_ATTEMPT_LIMIT = WAKE_TIMEOUT_SECS // PING_INTERVAL_SECS

SIGNAL_COLORS = {
    "bullish": "#00c48c",
    "bearish": "#ff4b4b",
    "neutral": "#a0a0b0",
}

SIGNAL_BG = {
    "bullish": "rgba(0,196,140,0.12)",
    "bearish": "rgba(255,75,75,0.12)",
    "neutral": "rgba(160,160,176,0.12)",
}

st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] { background: #0e1117; }
    [data-testid="stSidebar"] {
        background: #13161e;
        border-right: 1px solid #1f2330;
    }
    [data-testid="stSidebar"] * { color: #e0e0f0 !important; }

    .brand-block { padding: 1.2rem 0 0.6rem 0; }
    .brand-title {
        font-size: 1.25rem; font-weight: 700; color: #ffffff !important;
        letter-spacing: 0.01em; margin: 0 0 0.15rem 0;
    }
    .brand-sub { font-size: 0.78rem; color: #7b8099 !important; margin: 0; }

    .stock-card {
        padding: 0.65rem 0.85rem; border-radius: 8px; margin-bottom: 0.4rem;
        border: 1px solid transparent; position: relative;
    }
    .stock-card-active {
        border-color: #3d5afe !important; background: #141929 !important;
    }
    .stock-card-ticker {
        font-size: 0.95rem; font-weight: 700; color: #e8eaf6 !important;
        margin: 0 0 0.15rem 0;
    }
    .stock-card-range { font-size: 0.7rem; color: #5c6180 !important; margin: 0; }
    .signal-badge {
        display: inline-block; padding: 0.12rem 0.55rem; border-radius: 100px;
        font-size: 0.65rem; font-weight: 700; letter-spacing: 0.04em;
        text-transform: uppercase; float: right; margin-top: 0.05rem;
    }

    .page-header {
        padding: 0.5rem 0 1.2rem 0; border-bottom: 1px solid #1f2330;
        margin-bottom: 1.2rem;
    }
    .ticker-name {
        font-size: 2rem; font-weight: 800; color: #ffffff;
        margin: 0 0 0.3rem 0; line-height: 1;
    }
    .meta-pill {
        display: inline-block; background: #1a1e2e; border: 1px solid #2a2e45;
        border-radius: 100px; padding: 0.18rem 0.7rem; font-size: 0.72rem;
        color: #8890b0; margin-right: 0.4rem; margin-bottom: 0.4rem;
    }

    .stat-block {
        text-align: center; padding: 0.8rem 1rem; background: #13161e;
        border: 1px solid #1f2330; border-radius: 10px;
    }
    .stat-value {
        font-size: 1.45rem; font-weight: 700; color: #e8eaf6;
        margin: 0; line-height: 1;
    }
    .stat-label {
        font-size: 0.7rem; color: #5c6180; margin: 0.25rem 0 0 0;
        text-transform: uppercase; letter-spacing: 0.06em;
    }

    .analysis-card {
        background: #13161e; border: 1px solid #1f2330; border-radius: 10px;
        padding: 1rem 1.2rem; margin-bottom: 1rem; border-left-width: 4px;
    }
    .analysis-card-header {
        display: flex; align-items: center; justify-content: space-between;
        margin-bottom: 0.75rem;
    }
    .analysis-date { font-size: 0.78rem; color: #5c6180; margin: 0; }
    .big-signal-badge {
        display: inline-block; padding: 0.3rem 1rem; border-radius: 100px;
        font-size: 0.82rem; font-weight: 700; letter-spacing: 0.06em;
        text-transform: uppercase;
    }
    .indicator-row { display: flex; gap: 1rem; margin-bottom: 0.75rem; }
    .indicator-block {
        flex: 1; background: #0e1117; border: 1px solid #1f2330;
        border-radius: 8px; padding: 0.55rem 0.85rem;
    }
    .indicator-label {
        font-size: 0.65rem; color: #5c6180; text-transform: uppercase;
        letter-spacing: 0.06em; margin: 0 0 0.2rem 0;
    }
    .indicator-value { font-size: 1.1rem; font-weight: 700; color: #e8eaf6; margin: 0; }
    .thesis-text { font-size: 0.85rem; color: #9098b8; line-height: 1.65; margin: 0; }

    .step-row {
        display: flex; align-items: center; gap: 0.6rem; padding: 0.4rem 0;
        font-size: 0.85rem; color: #5c6180;
    }
    .step-done { color: #00c48c !important; }
    .step-active { color: #e8eaf6 !important; }
    .step-icon { font-size: 0.9rem; width: 1.2rem; text-align: center; }

    .wake-title {
        font-size: 1.4rem; font-weight: 700; color: #e8eaf6;
        margin: 1rem 0 0.4rem 0;
    }
    .wake-sub { font-size: 0.85rem; color: #5c6180; margin: 0 0 1.5rem 0; }

    .section-label {
        font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em;
        color: #3d4460; margin: 0.6rem 0 0.5rem 0; font-weight: 600;
    }

    [data-testid="stTabs"] button { font-weight: 600; font-size: 0.85rem; color: #5c6180; }
    [data-testid="stTabs"] button[aria-selected="true"] { color: #e8eaf6; }

    hr { border-color: #1f2330 !important; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)


for key, default in [
    ("backend_ready", False),
    ("ping_attempts", 0),
    ("selected_stock", None),
    ("selected_period", "3M"),
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

    _, center_col, _ = st.columns([1, 2, 1])
    with center_col:
        st.markdown(
            """
            <div style="text-align:center;padding:4rem 0 1rem 0;">
                <div style="font-size:3rem;">📈</div>
                <p class="wake-title">Starting up the backend…</p>
                <p class="wake-sub">
                    Free-tier services sleep when idle. This usually takes 30–60 seconds.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.progress(
            min(attempts / PING_ATTEMPT_LIMIT, 1.0),
            text=f"Attempt {attempts + 1} of {PING_ATTEMPT_LIMIT}",
        )

    try:
        resp = requests.get(f"{BACKEND_URL}/ping", timeout=PING_INTERVAL_SECS)
        resp.raise_for_status()
        st.session_state.backend_ready = True
        st.session_state.ping_attempts = 0
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


@st.cache_data(ttl=30)
def latest_signal(ticker: str) -> str:
    analyses = fetch_analyses(ticker)
    if analyses:
        return analyses[0].get("signal", "neutral").lower()
    return "neutral"


with st.spinner(""):
    stocks = fetch_stocks()

if not stocks:
    st.markdown(
        """
        <div style="text-align:center;padding:4rem 2rem;">
            <div style="font-size:3rem;margin-bottom:1rem;">📭</div>
            <h2 style="color:#e8eaf6;">No stocks found</h2>
            <p style="color:#5c6180;">Ingest stock CSV data via the backend to get started.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.stop()

stock_map: dict[str, dict] = {s["ticker"]: s for s in stocks}
ticker_options = sorted(stock_map.keys())

if st.session_state.selected_stock not in ticker_options:
    st.session_state.selected_stock = ticker_options[0]


with st.sidebar:
    st.markdown(
        """
        <div class="brand-block">
            <p class="brand-title">AI Equity Research</p>
            <p class="brand-sub">Technical signals &amp; Gemini-powered theses</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()
    st.markdown('<p class="section-label">Portfolio</p>', unsafe_allow_html=True)

    search_query = st.text_input(
        "Search",
        placeholder="Filter by ticker…",
        label_visibility="collapsed",
        key="ticker_search",
    )

    filtered_tickers = (
        [t for t in ticker_options if search_query.upper() in t] if search_query else ticker_options
    )

    if not filtered_tickers:
        st.caption("No stocks match your search.")
    else:
        for ticker in filtered_tickers:
            info = stock_map[ticker]
            sig = latest_signal(ticker)
            s_color = SIGNAL_COLORS.get(sig, SIGNAL_COLORS["neutral"])
            s_bg = SIGNAL_BG.get(sig, SIGNAL_BG["neutral"])
            is_active = ticker == st.session_state.selected_stock
            card_class = "stock-card stock-card-active" if is_active else "stock-card"

            st.markdown(
                f"""
                <div class="{card_class}">
                    <span class="signal-badge" style="background:{s_bg};color:{s_color};">
                        {sig}
                    </span>
                    <p class="stock-card-ticker">{ticker}</p>
                    <p class="stock-card-range">
                        {info.get("min_date", "—")} → {info.get("max_date", "—")}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button(
                ticker,
                key=f"select_{ticker}",
                use_container_width=True,
                help=f"View {ticker}",
            ):
                st.session_state.selected_stock = ticker
                st.rerun()

    st.divider()
    if st.button("Refresh data", use_container_width=True):
        fetch_stocks.clear()
        fetch_analyses.clear()
        fetch_ohlc.clear()
        latest_signal.clear()
        st.rerun()


selected_ticker: str = st.session_state.selected_stock
stock_info = stock_map.get(selected_ticker, {})

analyses = fetch_analyses(selected_ticker)
ohlc_response = fetch_ohlc(selected_ticker)
ohlc_data = ohlc_response.get("data", [])

latest_close = ohlc_data[-1]["close"] if ohlc_data else None
latest_sig = analyses[0].get("signal", "neutral").lower() if analyses else "neutral"


name = stock_info.get("name") or ""
sector = stock_info.get("sector") or ""
exchange = stock_info.get("exchange") or ""

pills_html = "".join(
    f'<span class="meta-pill">{label}</span>' for label in [name, sector, exchange] if label
)
if not pills_html:
    pills_html = '<span class="meta-pill">No metadata</span>'

price_str = f"${latest_close:,.2f}" if latest_close else "—"

st.markdown(
    f"""
    <div class="page-header">
        <div style="display:flex;align-items:flex-start;justify-content:space-between;
                    flex-wrap:wrap;gap:1rem;">
            <div>
                <p class="ticker-name">{selected_ticker}</p>
                <div>{pills_html}</div>
            </div>
            <div style="display:flex;gap:0.75rem;flex-shrink:0;">
                <div class="stat-block">
                    <p class="stat-value">{price_str}</p>
                    <p class="stat-label">Latest Close</p>
                </div>
                <div class="stat-block">
                    <p class="stat-value">{len(ohlc_data)}</p>
                    <p class="stat-label">Trading Days</p>
                </div>
                <div class="stat-block">
                    <p class="stat-value">{len(analyses)}</p>
                    <p class="stat-label">Analyses Run</p>
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


if ohlc_data:
    dates = [d["date"] for d in ohlc_data]
    opens = [d["open"] for d in ohlc_data]
    highs = [d["high"] for d in ohlc_data]
    lows = [d["low"] for d in ohlc_data]
    closes = [d["close"] for d in ohlc_data]
    volumes = [d.get("volume", 0) for d in ohlc_data]
    vol_colors = ["#00c48c" if closes[i] >= opens[i] else "#ff4b4b" for i in range(len(closes))]

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.72, 0.28],
    )

    fig.add_trace(
        go.Candlestick(
            x=dates,
            open=opens,
            high=highs,
            low=lows,
            close=closes,
            name="Price",
            increasing_line_color="#00c48c",
            decreasing_line_color="#ff4b4b",
            increasing_fillcolor="#00c48c",
            decreasing_fillcolor="#ff4b4b",
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Bar(
            x=dates,
            y=volumes,
            name="Volume",
            marker_color=vol_colors,
            opacity=0.7,
            showlegend=False,
        ),
        row=2,
        col=1,
    )

    dark_bg = "#0e1117"
    grid_color = "#1f2330"
    text_color = "#5c6180"

    fig.update_layout(
        height=500,
        paper_bgcolor=dark_bg,
        plot_bgcolor=dark_bg,
        margin=dict(l=0, r=0, t=8, b=0),
        xaxis_rangeslider_visible=False,
        showlegend=False,
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            tickfont=dict(color=text_color, size=11),
            rangeselector=dict(
                buttons=[
                    dict(count=1, label="1M", step="month", stepmode="backward"),
                    dict(count=3, label="3M", step="month", stepmode="backward"),
                    dict(count=6, label="6M", step="month", stepmode="backward"),
                    dict(count=1, label="1Y", step="year", stepmode="backward"),
                    dict(step="all", label="All"),
                ],
                bgcolor="#13161e",
                activecolor="#3d5afe",
                bordercolor="#1f2330",
                font=dict(color=text_color, size=11),
                x=0,
                y=1.02,
            ),
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=grid_color,
            zeroline=False,
            showline=False,
            tickfont=dict(color=text_color, size=11),
            side="right",
        ),
        xaxis2=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            tickfont=dict(color=text_color, size=11),
        ),
        yaxis2=dict(
            showgrid=True,
            gridcolor=grid_color,
            zeroline=False,
            showline=False,
            tickfont=dict(color=text_color, size=11),
            side="right",
        ),
        font=dict(family="Inter, sans-serif"),
        hoverlabel=dict(bgcolor="#13161e", bordercolor="#2a2e45", font_color="#e8eaf6"),
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.markdown(
        """
        <div style="text-align:center;padding:3rem 1rem;background:#13161e;
                    border:1px solid #1f2330;border-radius:10px;margin-bottom:1rem;">
            <div style="font-size:2rem;margin-bottom:0.5rem;">📉</div>
            <p style="color:#5c6180;margin:0;">No OHLC data available for this stock.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown("<div style='padding-top:0.5rem'></div>", unsafe_allow_html=True)

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "history"

tab_cols = st.columns([1, 1, 6])
with tab_cols[0]:
    history_active = st.session_state.active_tab == "history"
    if st.button(
        "📊 Analysis History",
        type="primary" if history_active else "secondary",
        use_container_width=True,
    ):
        st.session_state.active_tab = "history"
        st.rerun()

with tab_cols[1]:
    new_active = st.session_state.active_tab == "new"
    if st.button(
        "▶️ New Analysis",
        type="primary" if new_active else "secondary",
        use_container_width=True,
    ):
        st.session_state.active_tab = "new"
        st.rerun()

st.markdown("<div style='margin-bottom:1rem'></div>", unsafe_allow_html=True)

if st.session_state.active_tab == "history":
    if not analyses:
        st.markdown(
            """
            <div style="text-align:center;padding:3rem 1rem;background:#13161e;
                        border:1px solid #1f2330;border-radius:10px;margin-top:1rem;">
                <div style="font-size:2rem;margin-bottom:0.5rem;">🔍</div>
                <p style="color:#e8eaf6;font-weight:600;margin:0 0 0.3rem 0;">No analyses yet</p>
                <p style="color:#5c6180;margin:0;font-size:0.85rem;">
                    Run a new analysis to generate technical signals and an AI investment thesis.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        for analysis in analyses:
            sig = analysis.get("signal", "neutral").lower()
            s_color = SIGNAL_COLORS.get(sig, SIGNAL_COLORS["neutral"])
            s_bg = SIGNAL_BG.get(sig, SIGNAL_BG["neutral"])
            rsi_val = float(analysis.get("rsi") or 0)
            macd_val = float(analysis.get("macd") or 0)
            d_start = analysis.get("date_range_start", "—")
            d_end = analysis.get("date_range_end", "—")
            created = analysis.get("created_at", "")[:16].replace("T", " ")
            summary = analysis.get("summary", "No summary available.")

            st.markdown(
                f"""
                <div class="analysis-card" style="border-left-color:{s_color};">
                    <div class="analysis-card-header">
                        <p class="analysis-date">
                            {d_start} → {d_end} &nbsp;·&nbsp; Generated {created}
                        </p>
                        <span class="big-signal-badge" style="background:{s_bg};color:{s_color};">
                            {sig.upper()}
                        </span>
                    </div>
                    <div class="indicator-row">
                        <div class="indicator-block">
                            <p class="indicator-label">RSI (14)</p>
                            <p class="indicator-value">{rsi_val:.2f}</p>
                        </div>
                        <div class="indicator-block">
                            <p class="indicator-label">MACD</p>
                            <p class="indicator-value">{macd_val:.4f}</p>
                        </div>
                        <div class="indicator-block">
                            <p class="indicator-label">Signal</p>
                            <p class="indicator-value" style="color:{s_color};">
                                {sig.capitalize()}
                            </p>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            with st.expander("View AI Thesis", expanded=False):
                st.markdown(
                    f'<p class="thesis-text">{summary}</p>',
                    unsafe_allow_html=True,
                )


else:
    st.markdown("<div style='padding-top:0.5rem'>", unsafe_allow_html=True)

    min_date = date.fromisoformat(stock_info.get("min_date", date.today().isoformat()))
    max_date = date.fromisoformat(stock_info.get("max_date", date.today().isoformat()))

    PERIODS: dict[str, timedelta | None] = {
        "7D": timedelta(days=7),
        "1M": timedelta(days=30),
        "3M": timedelta(days=90),
        "6M": timedelta(days=180),
        "1Y": timedelta(days=365),
        "Custom": None,
    }

    st.markdown('<p class="section-label">Analysis Period</p>', unsafe_allow_html=True)

    period_cols = st.columns(len(PERIODS))
    for idx, period_label in enumerate(PERIODS):
        with period_cols[idx]:
            is_sel = st.session_state.selected_period == period_label
            if st.button(
                period_label,
                key=f"period_{period_label}",
                type="primary" if is_sel else "secondary",
                use_container_width=True,
            ):
                st.session_state.selected_period = period_label
                st.rerun()

    selected_period = st.session_state.selected_period
    end_date = max_date

    if selected_period == "Custom":
        c1, c2 = st.columns(2)
        with c1:
            start_date = st.date_input(
                "Start date",
                value=min_date,
                min_value=min_date,
                max_value=max_date,
                key="custom_start",
            )
        with c2:
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

    st.markdown(
        f"""
        <div style="background:#13161e;border:1px solid #1f2330;border-radius:8px;
                    padding:0.6rem 1rem;margin:0.75rem 0 1rem 0;display:inline-block;">
            <span style="color:#5c6180;font-size:0.75rem;text-transform:uppercase;
                         letter-spacing:0.06em;">Date range &nbsp;</span>
            <span style="color:#e8eaf6;font-weight:600;font-size:0.85rem;">
                {start_date.isoformat()} → {end_date.isoformat()}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    run_col, _ = st.columns([1, 3])
    with run_col:
        run_clicked = st.button("Run Analysis", type="primary", use_container_width=True)

    if run_clicked:
        payload = {
            "tickers": [selected_ticker],
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        }

        pipeline_steps = [
            "Fetching OHLC data",
            "Computing indicators (RSI / MACD)",
            "Generating AI thesis with Gemini",
            "Saving results to database",
        ]

        st.markdown("<br>", unsafe_allow_html=True)
        step_placeholder = st.empty()

        def render_steps(current: int) -> None:
            html = "<div>"
            for i, label in enumerate(pipeline_steps):
                if i < current:
                    icon, cls = "✓", "step-done"
                elif i == current:
                    icon, cls = "›", "step-active"
                else:
                    icon, cls = "○", ""
                html += (
                    f'<div class="step-row {cls}">'
                    f'<span class="step-icon">{icon}</span>'
                    f"<span>{label}</span>"
                    f"</div>"
                )
            html += "</div>"
            step_placeholder.markdown(html, unsafe_allow_html=True)

        render_steps(0)

        with st.spinner("Running analysis pipeline…"):
            api_response = requests.post(
                f"{BACKEND_URL}/analyze",
                data=json.dumps(payload),
                headers={"Content-Type": "application/json"},
                timeout=180,
            )

        if api_response.ok:
            render_steps(len(pipeline_steps))
            result_data = api_response.json()

            for result in result_data.get("results", []):
                indicators = result.get("indicators", {})
                r_rsi = float(indicators.get("rsi") or 0)
                r_macd = float(indicators.get("macd") or 0)
                r_sig = (indicators.get("signal") or "neutral").lower()
                r_thesis = result.get("thesis", "No thesis generated.")
                r_color = SIGNAL_COLORS.get(r_sig, SIGNAL_COLORS["neutral"])
                r_bg = SIGNAL_BG.get(r_sig, SIGNAL_BG["neutral"])

                st.markdown(
                    f"""
                    <div class="analysis-card"
                         style="border-left-color:{r_color};margin-top:1rem;">
                        <div class="analysis-card-header">
                            <p class="analysis-date">
                                {start_date.isoformat()} → {end_date.isoformat()}
                                &nbsp;·&nbsp; Just now
                            </p>
                            <span class="big-signal-badge"
                                  style="background:{r_bg};color:{r_color};">
                                {r_sig.upper()}
                            </span>
                        </div>
                        <div class="indicator-row">
                            <div class="indicator-block">
                                <p class="indicator-label">RSI (14)</p>
                                <p class="indicator-value">{r_rsi:.2f}</p>
                            </div>
                            <div class="indicator-block">
                                <p class="indicator-label">MACD</p>
                                <p class="indicator-value">{r_macd:.4f}</p>
                            </div>
                            <div class="indicator-block">
                                <p class="indicator-label">Signal</p>
                                <p class="indicator-value" style="color:{r_color};">
                                    {r_sig.capitalize()}
                                </p>
                            </div>
                        </div>
                        <p class="thesis-text">{r_thesis}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            fetch_analyses.clear()
            latest_signal.clear()
        else:
            step_placeholder.empty()
            st.error(f"Analysis failed: {api_response.text}")

    st.markdown("</div>", unsafe_allow_html=True)
