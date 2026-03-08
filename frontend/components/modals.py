import streamlit as st

from utils.helpers import get_signal_color


def render_wake_screen(attempts: int, max_attempts: int) -> None:
    _, center_col, _ = st.columns([1, 2, 1])
    with center_col:
        st.markdown(
            """
            <div class="wake-container">
                <div class="wake-icon">📈</div>
                <p class="wake-title">Starting up the backend…</p>
                <p class="wake-subtitle">
                    Free-tier services sleep when idle. This usually takes up to 60 seconds.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        progress_value = min(attempts / max_attempts, 1.0)
        st.progress(
            progress_value,
            text=f"Attempt {attempts + 1} of {max_attempts}",
        )


def render_step_progress(current_step: int, total_steps: int, steps: list[str]) -> None:
    html = "<div class='step-progress'>"
    for i, label in enumerate(steps):
        if i < current_step:
            icon, cls = "✓", "step-done"
        elif i == current_step:
            icon, cls = "▶", "step-active"
        else:
            icon, cls = "○", ""
        html += (
            f'<div class="step-row {cls}">'
            f'<span class="step-icon">{icon}</span>'
            f'<span class="step-label">{label}</span>'
            f"</div>"
        )
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def render_error_state(message: str) -> None:
    st.error(f"❌ {message}")


def render_success_result(
    start_date: str,
    end_date: str,
    rsi: float,
    macd: float,
    signal: str,
    thesis: str,
) -> None:
    signal_color, signal_bg = get_signal_color(signal)

    st.markdown(
        f"""
        <div class="analysis-card" style="--signal-color: {signal_color}; margin-top: 1rem;">
            <div class="analysis-card-header">
                <p class="analysis-date">
                    {start_date} → {end_date}
                    &nbsp;·&nbsp; Just now
                </p>
                <span class="analysis-signal-badge" style="background: {signal_bg}; color: {signal_color};">
                    {signal.upper()}
                </span>
            </div>
            <div class="analysis-indicators">
                <div class="analysis-indicator">
                    <p class="analysis-indicator-label">RSI (14)</p>
                    <p class="analysis-indicator-value">{rsi:.2f}</p>
                </div>
                <div class="analysis-indicator">
                    <p class="analysis-indicator-label">MACD</p>
                    <p class="analysis-indicator-value">{macd:.4f}</p>
                </div>
                <div class="analysis-indicator">
                    <p class="analysis-indicator-label">Signal</p>
                    <p class="analysis-indicator-value" style="color: {signal_color};">
                        {signal.capitalize()}
                    </p>
                </div>
            </div>
            <p class="thesis-text">{thesis}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
