from datetime import date, timedelta
from typing import Any, Callable

import streamlit as st

from styles.theme import COLORS
from utils.helpers import get_signal_color


def render_indicators_panel(
    ticker: str,
    analyses: list[dict[str, Any]],
    stock_info: dict[str, Any],
    on_run_analysis: Callable,
) -> None:
    st.markdown(
        """
        <p class="indicators-panel-title">Technical Indicators</p>
        """,
        unsafe_allow_html=True,
    )

    if analyses and len(analyses) > 0:
        latest = analyses[0]
        indicators = latest.get("indicators", {})
        rsi = float(indicators.get("rsi", 0))
        macd = float(indicators.get("macd", 0))
        signal = (indicators.get("signal") or "neutral").lower()
        signal_color, signal_bg = get_signal_color(signal)

        rsi_pct = min(100, max(0, rsi))
        if rsi > 70:
            rsi_bar_color = COLORS["bearish"]
        elif rsi < 30:
            rsi_bar_color = COLORS["bullish"]
        else:
            rsi_bar_color = COLORS["accent_primary"]

        st.markdown(
            f"""
            <div class="indicator-card">
                <p class="indicator-label">RSI (14)</p>
                <p class="indicator-value">{rsi:.2f}</p>
                <div class="indicator-bar">
                    <div class="indicator-bar-fill" style="width: {rsi_pct}%; background: {rsi_bar_color};"></div>
                </div>
                <div class="indicator-zone-labels">
                    <span>Oversold</span><span>Neutral</span><span>Overbought</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        macd_pct = min(100, max(0, (macd + 10) * 5))
        macd_color = (
            COLORS["bullish"] if macd > 0 else COLORS["bearish"] if macd < 0 else COLORS["neutral"]
        )

        st.markdown(
            f"""
            <div class="indicator-card">
                <p class="indicator-label">MACD</p>
                <p class="indicator-value">{macd:.4f}</p>
                <div class="indicator-bar">
                    <div class="indicator-bar-fill" style="width: {macd_pct}%; background: {macd_color};"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        signal_class = signal
        st.markdown(
            f"""
            <div class="indicator-card">
                <p class="indicator-label">Signal</p>
                <div class="signal-badge-large {signal_class}" style="background: {signal_bg}; color: {signal_color}; border: 1px solid {signal_color}40;">
                    {signal.upper()}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="indicator-card indicator-card-empty">
                <p class="indicator-empty-text">
                    No indicators yet.<br>Run an analysis below to see RSI, MACD, and signals.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div class='indicators-divider'></div>", unsafe_allow_html=True)

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

    if "selected_period" not in st.session_state:
        st.session_state.selected_period = "3M"

    st.markdown(
        "<p class='period-label'>Analysis Period</p>",
        unsafe_allow_html=True,
    )

    # Create a 3x2 grid for period buttons
    period_cols_1 = st.columns(3)
    period_cols_2 = st.columns(3)

    period_keys = list(PERIODS.keys())

    # First row: 7D, 1M, 3M
    for idx, period_label in enumerate(period_keys[:3]):
        with period_cols_1[idx]:
            is_sel = st.session_state.selected_period == period_label
            if st.button(
                period_label,
                key=f"period_{period_label}",
                type="primary" if is_sel else "secondary",
                use_container_width=True,
            ):
                st.session_state.selected_period = period_label
                st.rerun()

    # Second row: 6M, 1Y, Custom
    for idx, period_label in enumerate(period_keys[3:]):
        with period_cols_2[idx]:
            is_sel = st.session_state.selected_period == period_label
            if st.button(
                period_label,
                key=f"period_{period_label}_2",
                type="primary" if is_sel else "secondary",
                use_container_width=True,
            ):
                st.session_state.selected_period = period_label
                st.rerun()

    selected_period = st.session_state.selected_period
    end_date: date = max_date

    if selected_period == "Custom":
        date_cols = st.columns(2)
        with date_cols[0]:
            start_date = st.date_input(
                "Start",
                value=min_date,
                min_value=min_date,
                max_value=max_date,
                key="custom_start",
                label_visibility="collapsed",
            )
        with date_cols[1]:
            end_date = st.date_input(
                "End",
                value=max_date,
                min_value=min_date,
                max_value=max_date,
                key="custom_end",
                label_visibility="collapsed",
            )
    else:
        offset = PERIODS[selected_period]
        if offset is not None:
            start_date = max(min_date, max_date - offset)
        else:
            start_date = min_date

    st.markdown(
        f"""
        <div class="date-range-display">
            <span class="date-range-label">Range</span>
            <span class="date-range-value">{start_date.isoformat()} <span class="date-range-arrow">→</span> {end_date.isoformat()}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "🚀 Run Analysis",
        type="primary",
        use_container_width=True,
        key="run_analysis_btn",
    ):
        on_run_analysis(start_date, end_date)
