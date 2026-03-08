from typing import Any

import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots

from styles.theme import COLORS


def render_chart_panel(ohlc_data: list[dict[str, Any]]) -> None:
    # Chart panel title
    st.markdown(
        """
        <p style="font-size: 0.75rem; font-weight: 600; color: #6b7280; text-transform: uppercase; letter-spacing: 0.1em; margin: 0 0 1rem 0; padding-bottom: 0.5rem; border-bottom: 1px solid #252a3a;">Price Chart</p>
        """,
        unsafe_allow_html=True,
    )

    if not ohlc_data:
        st.markdown(
            """
            <div class="empty-state">
                <div class="empty-icon">📉</div>
                <p class="empty-title">No OHLC Data</p>
                <p class="empty-text">No price data available for this stock.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    dates = [d["date"] for d in ohlc_data]
    opens = [d["open"] for d in ohlc_data]
    highs = [d["high"] for d in ohlc_data]
    lows = [d["low"] for d in ohlc_data]
    closes = [d["close"] for d in ohlc_data]
    volumes = [d.get("volume", 0) for d in ohlc_data]
    vol_colors = [
        COLORS["bullish"] if closes[i] >= opens[i] else COLORS["bearish"]
        for i in range(len(closes))
    ]

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
            increasing_line_color=COLORS["bullish"],
            decreasing_line_color=COLORS["bearish"],
            increasing_fillcolor=COLORS["bullish"],
            decreasing_fillcolor=COLORS["bearish"],
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

    text_color = COLORS["text_muted"]
    grid_color = COLORS["border_primary"]

    fig.update_layout(
        height=520,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
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
                bgcolor=COLORS["bg_secondary"],
                activecolor=COLORS["accent_primary"],
                bordercolor=COLORS["border_primary"],
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
        hoverlabel=dict(
            bgcolor=COLORS["bg_secondary"],
            bordercolor=COLORS["border_secondary"],
            font_color=COLORS["text_primary"],
        ),
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
