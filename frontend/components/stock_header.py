from typing import Any

import streamlit as st

from styles.theme import COLORS
from utils.helpers import format_price, calculate_price_change


def render_stock_header(
    ticker: str,
    stock_info: dict[str, Any],
    ohlc_data: list[dict[str, Any]],
    analyses: list[dict[str, Any]],
) -> None:
    name = stock_info.get("name") or ""
    sector = stock_info.get("sector") or ""
    exchange = stock_info.get("exchange") or ""

    latest_close = ohlc_data[-1]["close"] if ohlc_data else None
    price_str = format_price(latest_close)

    change, change_pct = calculate_price_change(ohlc_data)
    change_str = f"{change:+,.2f}" if change is not None else "—"
    change_pct_str = f"{change_pct:+.2f}%" if change_pct is not None else "—%"
    change_color = (
        COLORS["bullish"]
        if change and change > 0
        else COLORS["bearish"]
        if change and change < 0
        else COLORS["text_muted"]
    )

    st.markdown(
        """
        <div class="stock-header-wrapper">
            <div class="stock-header">
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <p class="stock-ticker-main">{ticker}</p>
        <p class="stock-company-name">{name if name else ticker}</p>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Stat cards using Streamlit columns for horizontal layout
    stats = [
        ("Latest Close", price_str, COLORS["text_primary"]),
        ("Change", change_str, change_color),
        ("Change %", change_pct_str, change_color),
        ("Trading Days", str(len(ohlc_data)), COLORS["text_primary"]),
        ("Analyses Run", str(len(analyses)), COLORS["text_primary"]),
    ]

    stat_cols = st.columns(5)
    for idx, (label, value, color) in enumerate(stats):
        with stat_cols[idx]:
            st.markdown(
                f"""
                <div class="stat-card">
                    <p class="stat-value" style="color: {color};">{value}</p>
                    <p class="stat-label">{label}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
