import streamlit as st

from utils.helpers import get_signal_color, get_latest_signal


def render_stock_list(
    ticker_options: list[str],
    stock_map: dict,
    selected_ticker: str,
    analyses_cache: dict,
) -> str:
    st.markdown("<div class='stock-search-wrapper'>", unsafe_allow_html=True)
    search_query = st.text_input(
        "Search",
        placeholder="🔍 Filter by ticker…",
        label_visibility="collapsed",
        key="ticker_search",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    filtered_tickers = (
        [t for t in ticker_options if search_query.upper() in t] if search_query else ticker_options
    )

    if not filtered_tickers:
        st.caption("No stocks match your search.")
        return selected_ticker

    st.markdown('<p class="stock-list-header">Portfolio</p>', unsafe_allow_html=True)

    for ticker in filtered_tickers:
        info = stock_map[ticker]
        analyses = analyses_cache.get(ticker, [])
        sig = get_latest_signal(analyses)
        s_color, s_bg = get_signal_color(sig)
        is_active = ticker == selected_ticker

        active_class = "active" if is_active else ""

        date_range = f"{info.get('min_date', '—')} → {info.get('max_date', '—')}"

        st.markdown(
            f"""
            <div class="stock-list-item {active_class}">
                <div class="stock-item-row">
                    <div class="stock-item-left">
                        <p class="stock-ticker">{ticker}</p>
                        <p class="stock-date-range">{date_range}</p>
                    </div>
                    <span class="stock-signal" style="background:{s_bg};color:{s_color};">
                        {sig}
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            ticker,
            key=f"select_{ticker}",
            use_container_width=True,
        ):
            st.session_state.selected_stock = ticker
            st.rerun()

    st.divider()

    if st.button("🔄 Refresh Data", use_container_width=True, type="secondary"):
        from utils.api import fetch_stocks, fetch_analyses, fetch_ohlc

        fetch_stocks.clear()
        fetch_analyses.clear()
        fetch_ohlc.clear()
        st.rerun()

    return selected_ticker
