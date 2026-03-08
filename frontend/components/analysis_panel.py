from typing import Any

import streamlit as st

from utils.helpers import get_signal_color


def render_analysis_panel(analyses: list[dict[str, Any]]) -> None:
    # Section header
    st.markdown(
        f"""
        <div class="analysis-section-header">
            <p class="analysis-title">
                Analysis History
                <span class="analysis-count">{len(analyses)}</span>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not analyses:
        st.markdown(
            """
            <div class="analysis-empty-state">
                <div class="empty-icon">🔍</div>
                <p class="empty-title">No Analyses Yet</p>
                <p class="empty-text">Run a new analysis to generate technical signals and an AI investment thesis.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # Analysis cards
    for analysis in analyses:
        sig = analysis.get("signal", "neutral").lower()
        s_color, s_bg = get_signal_color(sig)
        rsi_val = float(analysis.get("rsi") or 0)
        macd_val = float(analysis.get("macd") or 0)
        d_start = analysis.get("date_range_start", "—")
        d_end = analysis.get("date_range_end", "—")
        created = analysis.get("created_at", "")[:16].replace("T", " ")
        summary = analysis.get("summary", "No summary available.")

        st.markdown(
            f"""
            <div class="analysis-card" style="--signal-color: {s_color};">
                <div class="analysis-card-header">
                    <p class="analysis-date">
                        {d_start} → {d_end} &nbsp;·&nbsp; {created}
                    </p>
                    <span class="analysis-signal-badge" style="background: {s_bg}; color: {s_color};">
                        {sig.upper()}
                    </span>
                </div>
                <div class="analysis-indicators">
                    <div class="analysis-indicator">
                        <p class="analysis-indicator-label">RSI (14)</p>
                        <p class="analysis-indicator-value">{rsi_val:.2f}</p>
                    </div>
                    <div class="analysis-indicator">
                        <p class="analysis-indicator-label">MACD</p>
                        <p class="analysis-indicator-value">{macd_val:.4f}</p>
                    </div>
                    <div class="analysis-indicator">
                        <p class="analysis-indicator-label">Signal</p>
                        <p class="analysis-indicator-value" style="color: {s_color};">
                            {sig.capitalize()}
                        </p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.expander("📄 View AI Thesis", expanded=False):
            st.markdown(
                f'<p class="thesis-text">{summary}</p>',
                unsafe_allow_html=True,
            )
