import streamlit as st


def render_top_nav(selected_ticker: str, ticker_options: list[str]) -> str:
    nav_cols = st.columns([2, 3, 2])

    with nav_cols[0]:
        st.markdown(
            """
            <div class="nav-logo">
                <span class="nav-logo-icon">📈</span>
                <span class="nav-logo-text">AI Equity Research</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with nav_cols[1]:
        if len(ticker_options) > 1:
            selected = st.selectbox(
                "Select Stock",
                options=ticker_options,
                index=ticker_options.index(selected_ticker)
                if selected_ticker in ticker_options
                else 0,
                key="nav_stock_selector",
                label_visibility="collapsed",
            )
            return selected
        else:
            st.markdown(
                f"<div class='nav-single-ticker'>{selected_ticker}</div>",
                unsafe_allow_html=True,
            )
            return selected_ticker

    with nav_cols[2]:
        # Empty column for balance
        pass

    return selected_ticker
