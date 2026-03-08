from .theme import COLORS, SPACING, TYPOGRAPHY, TRANSITIONS, LAYOUT

GLOBAL_STYLES = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    *, *::before, *::after {{
        font-family: {TYPOGRAPHY["font_family"]};
        box-sizing: border-box;
    }}

    /* ── App shell ───────────────────────────────────────────── */
    [data-testid="stAppViewContainer"] {{
        background: {COLORS["bg_primary"]} !important;
    }}

    [data-testid="stMain"] {{
        background: {COLORS["bg_primary"]} !important;
    }}

    /* Hide Streamlit chrome */
    [data-testid="stHeader"] {{
        display: none !important;
    }}

    #MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"] {{
        display: none !important;
        visibility: hidden !important;
    }}

    /* Main content container */
    .main .block-container {{
        padding: 0.5rem 1.5rem 2rem 1.5rem !important;
        max-width: {LAYOUT["max_content_width"]} !important;
    }}

    /* Analysis section wrapper */
    .analysis-section-wrapper {{
        margin-top: {SPACING["xl"]};
    }}

    /* ── Main content columns styling ─────────────────────────── */
    /* Target the first column (chart) */
    [data-testid="stHorizontalBlock"] > [data-testid="column"]:first-child {{
        background: {COLORS["bg_card"]};
        border: 1px solid {COLORS["border_primary"]};
        border-radius: 12px;
        padding: {SPACING["md"]};
        min-height: 550px;
        margin-top: {SPACING["xl"]};
    }}

    /* Target the second column (indicators) */
    [data-testid="stHorizontalBlock"] > [data-testid="column"]:nth-child(2) {{
        background: {COLORS["bg_card"]};
        border: 1px solid {COLORS["border_primary"]};
        border-radius: 12px;
        padding: {SPACING["md"]};
        margin-top: {SPACING["xl"]};
    }}

    /* ── Sidebar ─────────────────────────────────────────────── */
    [data-testid="stSidebar"] {{
        background: {COLORS["bg_secondary"]} !important;
        border-right: 1px solid {COLORS["border_primary"]} !important;
        min-width: {LAYOUT["sidebar_width"]} !important;
        max-width: {LAYOUT["sidebar_width"]} !important;
    }}

    [data-testid="stSidebarContent"] {{
        padding: 1rem !important;
    }}

    [data-testid="stSidebar"] .block-container {{
        padding: 0 !important;
    }}

    /* ── Text inputs ─────────────────────────────────────────── */
    [data-testid="stTextInput"] > div > div > input {{
        background: {COLORS["bg_tertiary"]} !important;
        border: 1px solid {COLORS["border_primary"]} !important;
        color: {COLORS["text_primary"]} !important;
        border-radius: 8px !important;
        padding: 0.6rem 0.75rem !important;
        font-size: {TYPOGRAPHY["sizes"]["sm"]} !important;
        transition: all {TRANSITIONS["fast"]} !important;
    }}

    [data-testid="stTextInput"] > div > div > input:focus {{
        border-color: {COLORS["accent_primary"]} !important;
        box-shadow: 0 0 0 3px rgba(79,106,247,0.15) !important;
    }}

    [data-testid="stTextInput"] > div > div > input::placeholder {{
        color: {COLORS["text_muted"]} !important;
    }}

    /* ── Selectbox ───────────────────────────────────────────── */
    [data-testid="stSelectbox"] > div > div {{
        background: {COLORS["bg_tertiary"]} !important;
        border: 1px solid {COLORS["border_primary"]} !important;
        color: {COLORS["text_primary"]} !important;
        border-radius: 8px !important;
    }}

    [data-testid="stSelectbox"] > div > div:hover {{
        border-color: {COLORS["border_secondary"]} !important;
    }}

    /* ── Divider ─────────────────────────────────────────────── */
    hr {{
        border-color: {COLORS["border_primary"]} !important;
        margin: {SPACING["md"]} 0 !important;
        opacity: 0.6;
    }}

    /* ── Expander ────────────────────────────────────────────── */
    [data-testid="stExpander"] {{
        background: {COLORS["bg_tertiary"]} !important;
        border: 1px solid {COLORS["border_primary"]} !important;
        border-radius: 8px !important;
        overflow: hidden;
    }}

    [data-testid="stExpander"] summary {{
        color: {COLORS["text_secondary"]} !important;
        font-size: {TYPOGRAPHY["sizes"]["sm"]} !important;
        font-weight: {TYPOGRAPHY["weights"]["medium"]} !important;
        padding: 0.75rem 1rem !important;
    }}

    [data-testid="stExpander"] summary:hover {{
        color: {COLORS["text_primary"]} !important;
        background: {COLORS["bg_hover"]};
    }}

    /* ── Vertical block spacing ──────────────────────────────── */
    [data-testid="stVerticalBlock"] {{
        gap: 0.5rem !important;
    }}

    /* ── Horizontal block spacing ────────────────────────────── */
    [data-testid="stHorizontalBlock"] {{
        gap: 1rem !important;
        align-items: flex-start !important;
    }}

    /* ── Caption ─────────────────────────────────────────────── */
    .stCaption {{
        color: {COLORS["text_muted"]} !important;
        font-size: {TYPOGRAPHY["sizes"]["xs"]} !important;
    }}
</style>
"""

BUTTON_STYLES = f"""
<style>
    /* ── Base button ─────────────────────────────────────────── */
    [data-testid="stButton"] > button {{
        border-radius: 8px !important;
        font-weight: {TYPOGRAPHY["weights"]["semibold"]} !important;
        font-size: {TYPOGRAPHY["sizes"]["sm"]} !important;
        transition: all {TRANSITIONS["fast"]} !important;
        padding: 0.5rem 1rem !important;
        line-height: 1.5 !important;
        border: 1px solid transparent !important;
    }}

    /* Primary — accent */
    [data-testid="stButton"] > button[kind="primary"] {{
        background: linear-gradient(135deg, {COLORS["accent_gradient_start"]} 0%, {COLORS["accent_gradient_end"]} 100%) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 2px 8px rgba(79,106,247,0.25) !important;
    }}

    [data-testid="stButton"] > button[kind="primary"]:hover {{
        background: linear-gradient(135deg, {COLORS["accent_hover"]} 0%, {COLORS["accent_gradient_end"]} 100%) !important;
        box-shadow: 0 4px 12px rgba(79,106,247,0.4) !important;
        transform: translateY(-1px);
    }}

    [data-testid="stButton"] > button[kind="primary"]:active {{
        transform: translateY(0);
        box-shadow: 0 2px 6px rgba(79,106,247,0.3) !important;
    }}

    /* Secondary */
    [data-testid="stButton"] > button[kind="secondary"] {{
        background: {COLORS["bg_tertiary"]} !important;
        color: {COLORS["text_secondary"]} !important;
        border: 1px solid {COLORS["border_primary"]} !important;
    }}

    [data-testid="stButton"] > button[kind="secondary"]:hover {{
        background: {COLORS["bg_hover"]} !important;
        color: {COLORS["text_primary"]} !important;
        border-color: {COLORS["border_secondary"]} !important;
    }}

    /* Sidebar buttons */
    [data-testid="stSidebar"] [data-testid="stButton"] > button {{
        background: transparent !important;
        border: none !important;
        color: transparent !important;
        padding: 0 !important;
        height: 0 !important;
        min-height: 0 !important;
        overflow: hidden;
    }}

    [data-testid="stSidebar"] [data-testid="stButton"]:last-of-type > button {{
        display: flex !important;
        background: {COLORS["bg_tertiary"]} !important;
        color: {COLORS["text_secondary"]} !important;
        border: 1px solid {COLORS["border_primary"]} !important;
        width: 100% !important;
        height: auto !important;
        min-height: 40px !important;
        justify-content: center !important;
        align-items: center !important;
        padding: 0.6rem !important;
        margin-top: 1rem !important;
        overflow: visible;
    }}

    [data-testid="stSidebar"] [data-testid="stButton"]:last-of-type > button:hover {{
        background: {COLORS["bg_hover"]} !important;
        color: {COLORS["text_primary"]} !important;
        border-color: {COLORS["border_secondary"]} !important;
    }}

    /* Period selector buttons */
    .period-button {{
        padding: 0.4rem 0.6rem !important;
        font-size: 0.75rem !important;
    }}

    /* Run Analysis button */
    .run-analysis-btn {{
        margin-top: {SPACING["md"]} !important;
    }}
</style>
"""

NAV_STYLES = f"""
<style>
    /* ── Top navigation styling ──────────────────────────────── */
    /* Target the first horizontal block (nav) specifically */
    .main .block-container > [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"]:first-of-type {{
        background: {COLORS["bg_card"]};
        border-bottom: 1px solid {COLORS["border_primary"]};
        padding: 0.75rem 1.5rem;
        margin: -0.5rem -1.5rem 1.5rem -1.5rem;
        position: sticky;
        top: 0;
        z-index: 100;
        backdrop-filter: blur(10px);
        border-radius: 0;
        min-height: auto;
    }}
    
    /* Remove background/padding from nav columns */
    .main .block-container > [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"]:first-of-type > [data-testid="column"] {{
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin-top: 0 !important;
        min-height: auto !important;
    }}

    /* ── Top navigation row ──────────────────────────────────── */
    .nav-logo {{
        display: flex;
        align-items: center;
        gap: {SPACING["sm"]};
        font-size: {TYPOGRAPHY["sizes"]["lg"]};
        font-weight: {TYPOGRAPHY["weights"]["bold"]};
        color: {COLORS["text_primary"]};
        padding: 0.5rem 0;
        white-space: nowrap;
    }}

    .nav-logo-icon {{
        font-size: 1.5rem;
        line-height: 1;
        filter: drop-shadow(0 0 8px rgba(79,106,247,0.4));
    }}

    .nav-logo-text {{
        background: linear-gradient(135deg, {COLORS["text_primary"]} 0%, {COLORS["accent_primary"]} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}

    .nav-single-ticker {{
        text-align: center;
        font-size: 1.25rem;
        font-weight: {TYPOGRAPHY["weights"]["bold"]};
        color: {COLORS["text_primary"]};
        padding: 0.5rem 0;
        letter-spacing: 0.02em;
    }}

    .nav-selector-wrapper {{
        display: flex;
        justify-content: center;
        align-items: center;
    }}
</style>
"""

STOCK_LIST_STYLES = f"""
<style>
    /* ── Sidebar stock list ──────────────────────────────────── */
    .stock-list-header {{
        font-size: {TYPOGRAPHY["sizes"]["xs"]} !important;
        text-transform: uppercase !important;
        letter-spacing: 0.12em !important;
        color: {COLORS["text_muted"]} !important;
        font-weight: {TYPOGRAPHY["weights"]["semibold"]} !important;
        margin: {SPACING["lg"]} 0 {SPACING["sm"]} 0 !important;
        padding: 0 !important;
    }}

    .stock-list-item {{
        padding: 0.6rem 0.75rem;
        border-radius: 8px;
        border-left: 3px solid transparent;
        margin-bottom: 4px;
        cursor: pointer;
        transition: all {TRANSITIONS["fast"]};
        background: transparent;
    }}

    .stock-list-item:hover {{
        background: {COLORS["bg_hover"]};
        border-left-color: {COLORS["border_secondary"]};
    }}

    .stock-list-item.active {{
        background: {COLORS["bg_tertiary"]};
        border-left-color: {COLORS["accent_primary"]};
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }}

    .stock-item-row {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.5rem;
    }}

    .stock-item-left {{
        flex: 1;
        min-width: 0;
    }}

    .stock-ticker {{
        font-size: {TYPOGRAPHY["sizes"]["base"]} !important;
        font-weight: {TYPOGRAPHY["weights"]["bold"]} !important;
        color: {COLORS["text_primary"]} !important;
        margin: 0 !important;
        line-height: 1.3 !important;
        letter-spacing: 0.01em;
    }}

    .stock-date-range {{
        font-size: 0.65rem !important;
        color: {COLORS["text_muted"]} !important;
        margin: 0.15rem 0 0 0 !important;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        line-height: 1.2 !important;
    }}

    .stock-signal {{
        flex-shrink: 0;
        padding: 0.15rem 0.5rem;
        border-radius: 100px;
        font-size: 0.65rem;
        font-weight: {TYPOGRAPHY["weights"]["bold"]};
        text-transform: uppercase;
        letter-spacing: 0.04em;
        white-space: nowrap;
    }}

    .stock-search-wrapper {{
        margin-bottom: {SPACING["md"]};
    }}
</style>
"""

STOCK_HEADER_STYLES = f"""
<style>
    /* ── Stock header wrapper ────────────────────────────────── */
    .stock-header-wrapper {{
        padding: {SPACING["md"]} 0;
        margin-bottom: {SPACING["md"]};
    }}

    /* ── Stock header (ticker section) ───────────────────────── */
    .stock-header {{
        margin-bottom: {SPACING["md"]};
        padding-bottom: {SPACING["md"]};
        border-bottom: 1px solid {COLORS["border_primary"]};
    }}

    .stock-ticker-main {{
        font-size: {TYPOGRAPHY["sizes"]["3xl"]} !important;
        font-weight: {TYPOGRAPHY["weights"]["extrabold"]} !important;
        color: {COLORS["text_primary"]} !important;
        margin: 0 !important;
        line-height: 1 !important;
        letter-spacing: -0.02em;
    }}

    .stock-company-name {{
        font-size: {TYPOGRAPHY["sizes"]["base"]} !important;
        color: {COLORS["text_secondary"]} !important;
        margin: 0.35rem 0 0.75rem 0 !important;
        line-height: 1.4 !important;
    }}

    .stock-meta-pills {{
        display: flex;
        gap: {SPACING["xs"]};
        flex-wrap: wrap;
    }}

    .meta-pill {{
        background: {COLORS["bg_tertiary"]};
        border: 1px solid {COLORS["border_primary"]};
        border-radius: 100px;
        padding: 0.2rem 0.7rem;
        font-size: {TYPOGRAPHY["sizes"]["xs"]};
        color: {COLORS["text_secondary"]};
        white-space: nowrap;
        transition: all {TRANSITIONS["fast"]};
    }}

    .meta-pill:hover {{
        border-color: {COLORS["border_secondary"]};
        color: {COLORS["text_primary"]};
    }}

    /* ── Stat cards ──────────────────────────────────────────── */
    .stats-container {{
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: {SPACING["sm"]};
    }}

    .stat-card {{
        background: {COLORS["bg_secondary"]};
        border: 1px solid {COLORS["border_primary"]};
        border-radius: 10px;
        padding: 0.875rem 0.5rem;
        text-align: center;
        transition: all {TRANSITIONS["fast"]};
    }}

    .stat-card:hover {{
        border-color: {COLORS["border_secondary"]};
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }}

    .stat-value {{
        font-size: 1.15rem !important;
        font-weight: {TYPOGRAPHY["weights"]["bold"]} !important;
        color: {COLORS["text_primary"]} !important;
        margin: 0 !important;
        line-height: 1.2 !important;
    }}

    .stat-label {{
        font-size: 0.65rem !important;
        color: {COLORS["text_muted"]} !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
        margin: 0.35rem 0 0 0 !important;
        line-height: 1.2 !important;
    }}

    @media (max-width: 768px) {{
        .stats-container {{
            grid-template-columns: repeat(3, 1fr);
        }}
    }}
</style>
"""

INDICATORS_PANEL_STYLES = f"""
<style>
    /* ── Indicators panel title ──────────────────────────────── */
    .indicators-panel-title {{
        font-size: {TYPOGRAPHY["sizes"]["xs"]} !important;
        font-weight: {TYPOGRAPHY["weights"]["semibold"]} !important;
        color: {COLORS["text_muted"]} !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        margin: 0 0 {SPACING["md"]} 0 !important;
        padding-bottom: {SPACING["sm"]};
        border-bottom: 1px solid {COLORS["border_primary"]};
    }}

    /* ── Indicator cards ─────────────────────────────────────── */
    .indicator-card {{
        background: {COLORS["bg_secondary"]};
        border: 1px solid {COLORS["border_primary"]};
        border-radius: 10px;
        padding: {SPACING["md"]};
        margin-bottom: {SPACING["md"]};
        transition: all {TRANSITIONS["fast"]};
    }}

    .indicator-card:hover {{
        border-color: {COLORS["border_secondary"]};
    }}

    .indicator-card-empty {{
        text-align: center;
        padding: 2rem {SPACING["md"]};
    }}

    .indicator-label {{
        font-size: 0.65rem !important;
        color: {COLORS["text_muted"]} !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
        margin: 0 0 0.5rem 0 !important;
        line-height: 1 !important;
        font-weight: {TYPOGRAPHY["weights"]["semibold"]} !important;
    }}

    .indicator-value {{
        font-size: 1.75rem !important;
        font-weight: {TYPOGRAPHY["weights"]["bold"]} !important;
        color: {COLORS["text_primary"]} !important;
        margin: 0 0 0.75rem 0 !important;
        line-height: 1 !important;
        letter-spacing: -0.02em;
    }}

    .indicator-bar {{
        height: 8px;
        background: {COLORS["bg_tertiary"]};
        border-radius: 4px;
        overflow: hidden;
        box-shadow: inset 0 1px 2px rgba(0,0,0,0.2);
    }}

    .indicator-bar-fill {{
        height: 100%;
        border-radius: 4px;
        transition: width 0.5s ease;
        box-shadow: 0 0 8px rgba(79,106,247,0.3);
    }}

    .indicator-zone-labels {{
        display: flex;
        justify-content: space-between;
        margin-top: 0.4rem;
    }}

    .indicator-zone-labels span {{
        font-size: 0.6rem !important;
        color: {COLORS["text_disabled"]} !important;
        font-weight: {TYPOGRAPHY["weights"]["medium"]} !important;
    }}

    .indicator-empty-text {{
        font-size: {TYPOGRAPHY["sizes"]["sm"]} !important;
        color: {COLORS["text_muted"]} !important;
        line-height: 1.7 !important;
        margin: 0 !important;
    }}

    /* ── Signal badge ────────────────────────────────────────── */
    .signal-badge-large {{
        display: block;
        padding: {SPACING["md"]};
        border-radius: 10px;
        font-size: 0.875rem;
        font-weight: {TYPOGRAPHY["weights"]["bold"]};
        text-transform: uppercase;
        letter-spacing: 0.15em;
        text-align: center;
        width: 100%;
        transition: all {TRANSITIONS["normal"]};
    }}

    .signal-badge-large.bullish {{
        box-shadow: 0 0 20px {COLORS["bullish_glow"]};
    }}

    .signal-badge-large.bearish {{
        box-shadow: 0 0 20px {COLORS["bearish_glow"]};
    }}

    /* ── Divider ─────────────────────────────────────────────── */
    .indicators-divider {{
        height: 1px;
        background: linear-gradient(90deg, transparent, {COLORS["border_primary"]}, transparent);
        margin: {SPACING["lg"]} 0;
    }}

    /* ── Period selector ─────────────────────────────────────── */
    .period-selector-wrapper {{
        margin-bottom: {SPACING["md"]};
    }}

    .period-label {{
        font-size: 0.65rem !important;
        color: {COLORS["text_muted"]} !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        margin: 0 0 {SPACING["sm"]} 0 !important;
        font-weight: {TYPOGRAPHY["weights"]["semibold"]} !important;
    }}

    .period-buttons-row {{
        display: flex;
        gap: 0.35rem;
        flex-wrap: wrap;
    }}

    .period-btn {{
        flex: 1;
        min-width: 45px;
    }}

    /* ── Date range display ──────────────────────────────────── */
    .date-range-display {{
        background: {COLORS["bg_secondary"]};
        border: 1px solid {COLORS["border_primary"]};
        border-radius: 8px;
        padding: 0.6rem 0.875rem;
        margin: {SPACING["md"]} 0;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }}

    .date-range-display:hover {{
        border-color: {COLORS["border_secondary"]};
    }}

    .date-range-label {{
        font-size: 0.65rem !important;
        color: {COLORS["text_muted"]} !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
        flex-shrink: 0;
        font-weight: {TYPOGRAPHY["weights"]["semibold"]} !important;
    }}

    .date-range-value {{
        font-size: {TYPOGRAPHY["sizes"]["sm"]} !important;
        font-weight: {TYPOGRAPHY["weights"]["semibold"]} !important;
        color: {COLORS["text_primary"]} !important;
        letter-spacing: 0.01em;
    }}

    .date-range-arrow {{
        color: {COLORS["text_muted"]};
        font-size: 0.75rem;
    }}
</style>
"""

ANALYSIS_PANEL_STYLES = f"""
<style>
    /* ── Analysis section header ─────────────────────────────── */
    .analysis-section-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 0 {SPACING["md"]} 0;
        border-bottom: 1px solid {COLORS["border_primary"]};
        margin-bottom: {SPACING["lg"]};
    }}

    .analysis-title {{
        font-size: {TYPOGRAPHY["sizes"]["lg"]} !important;
        font-weight: {TYPOGRAPHY["weights"]["semibold"]} !important;
        color: {COLORS["text_primary"]} !important;
        margin: 0 !important;
        letter-spacing: -0.01em;
    }}

    .analysis-count {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: {COLORS["bg_tertiary"]};
        color: {COLORS["text_secondary"]} !important;
        font-size: {TYPOGRAPHY["sizes"]["sm"]} !important;
        font-weight: {TYPOGRAPHY["weights"]["medium"]} !important;
        padding: 0.2rem 0.6rem;
        border-radius: 100px;
        margin-left: {SPACING["sm"]} !important;
        min-width: 28px;
    }}

    /* ── Analysis cards grid ─────────────────────────────────── */
    .analysis-cards-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
        gap: {SPACING["md"]};
    }}

    @media (max-width: 768px) {{
        .analysis-cards-grid {{
            grid-template-columns: 1fr;
        }}
    }}

    /* ── Analysis cards ──────────────────────────────────────── */
    .analysis-card {{
        background: {COLORS["bg_card"]};
        border: 1px solid {COLORS["border_primary"]};
        border-radius: 12px;
        padding: {SPACING["md"]};
        transition: all {TRANSITIONS["normal"]};
        position: relative;
        overflow: hidden;
    }}

    .analysis-card::before {{
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 4px;
        background: var(--signal-color, {COLORS["neutral"]});
        opacity: 0.8;
    }}

    .analysis-card:hover {{
        border-color: {COLORS["border_secondary"]};
        box-shadow: 0 4px 20px rgba(0,0,0,0.25);
        transform: translateY(-2px);
    }}

    .analysis-card-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: {SPACING["md"]};
        gap: {SPACING["sm"]};
        padding-left: {SPACING["sm"]};
    }}

    .analysis-date {{
        font-size: {TYPOGRAPHY["sizes"]["xs"]} !important;
        color: {COLORS["text_muted"]} !important;
        margin: 0 !important;
        line-height: 1.4 !important;
    }}

    .analysis-signal-badge {{
        padding: 0.25rem 0.75rem;
        border-radius: 100px;
        font-size: {TYPOGRAPHY["sizes"]["xs"]};
        font-weight: {TYPOGRAPHY["weights"]["bold"]};
        text-transform: uppercase;
        letter-spacing: 0.06em;
        white-space: nowrap;
        flex-shrink: 0;
        transition: all {TRANSITIONS["fast"]};
    }}

    .analysis-indicators {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: {SPACING["sm"]};
        margin-bottom: {SPACING["md"]};
        padding-left: {SPACING["sm"]};
    }}

    .analysis-indicator {{
        background: {COLORS["bg_secondary"]};
        border: 1px solid {COLORS["border_primary"]};
        border-radius: 8px;
        padding: {SPACING["sm"]};
        text-align: center;
        transition: all {TRANSITIONS["fast"]};
    }}

    .analysis-indicator:hover {{
        border-color: {COLORS["border_secondary"]};
        background: {COLORS["bg_tertiary"]};
    }}

    .analysis-indicator-label {{
        font-size: 0.6rem !important;
        color: {COLORS["text_muted"]} !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        margin: 0 0 0.25rem 0 !important;
        line-height: 1 !important;
        font-weight: {TYPOGRAPHY["weights"]["semibold"]} !important;
    }}

    .analysis-indicator-value {{
        font-size: {TYPOGRAPHY["sizes"]["base"]} !important;
        font-weight: {TYPOGRAPHY["weights"]["bold"]} !important;
        color: {COLORS["text_primary"]} !important;
        margin: 0 !important;
        line-height: 1.3 !important;
    }}

    .thesis-text {{
        font-size: {TYPOGRAPHY["sizes"]["sm"]} !important;
        color: {COLORS["text_secondary"]} !important;
        line-height: 1.8 !important;
        margin: 0 !important;
        padding-left: {SPACING["sm"]};
    }}

    /* ── Empty state ─────────────────────────────────────────── */
    .analysis-empty-state {{
        text-align: center;
        padding: 3rem 2rem;
        background: {COLORS["bg_card"]};
        border: 1px solid {COLORS["border_primary"]};
        border-radius: 12px;
        border-style: dashed;
    }}
</style>
"""

WAKE_SCREEN_STYLES = f"""
<style>
    .wake-container {{
        text-align: center;
        padding: 5rem 2rem 3rem;
        max-width: 500px;
        margin: 0 auto;
    }}

    .wake-icon {{
        font-size: 4rem;
        line-height: 1;
        margin-bottom: {SPACING["lg"]};
        filter: drop-shadow(0 0 20px rgba(79,106,247,0.4));
        animation: pulse 2s ease-in-out infinite;
    }}

    @keyframes pulse {{
        0%, 100% {{ opacity: 1; transform: scale(1); }}
        50% {{ opacity: 0.8; transform: scale(1.05); }}
    }}

    .wake-title {{
        font-size: {TYPOGRAPHY["sizes"]["2xl"]} !important;
        font-weight: {TYPOGRAPHY["weights"]["bold"]} !important;
        color: {COLORS["text_primary"]} !important;
        margin: 0 0 {SPACING["sm"]} 0 !important;
        letter-spacing: -0.02em;
    }}

    .wake-subtitle {{
        font-size: {TYPOGRAPHY["sizes"]["base"]} !important;
        color: {COLORS["text_secondary"]} !important;
        margin: 0 0 {SPACING["xl"]} 0 !important;
        line-height: 1.7 !important;
    }}

    .wake-progress {{
        background: {COLORS["bg_tertiary"]} !important;
        border-radius: 100px !important;
        height: 6px !important;
    }}

    .wake-progress-bar {{
        background: linear-gradient(90deg, {COLORS["accent_gradient_start"]}, {COLORS["accent_gradient_end"]}) !important;
        border-radius: 100px !important;
    }}
</style>
"""

EMPTY_STATE_STYLES = f"""
<style>
    .empty-state {{
        text-align: center;
        padding: 4rem 2rem;
        background: {COLORS["bg_card"]};
        border: 1px solid {COLORS["border_primary"]};
        border-radius: 12px;
        border-style: dashed;
    }}

    .empty-icon {{
        font-size: 3rem;
        line-height: 1;
        margin-bottom: {SPACING["md"]};
        opacity: 0.8;
    }}

    .empty-title {{
        font-size: {TYPOGRAPHY["sizes"]["lg"]} !important;
        font-weight: {TYPOGRAPHY["weights"]["semibold"]} !important;
        color: {COLORS["text_primary"]} !important;
        margin: 0 0 {SPACING["xs"]} 0 !important;
    }}

    .empty-text {{
        font-size: {TYPOGRAPHY["sizes"]["base"]} !important;
        color: {COLORS["text_secondary"]} !important;
        margin: 0 !important;
        line-height: 1.6 !important;
    }}
</style>
"""

STEP_PROGRESS_STYLES = f"""
<style>
    .step-progress {{
        background: {COLORS["bg_card"]};
        border: 1px solid {COLORS["border_primary"]};
        border-radius: 12px;
        padding: {SPACING["lg"]};
        margin: {SPACING["md"]} 0;
    }}

    .step-row {{
        display: flex;
        align-items: center;
        gap: {SPACING["md"]};
        padding: {SPACING["sm"]} 0;
        font-size: {TYPOGRAPHY["sizes"]["base"]} !important;
        color: {COLORS["text_muted"]};
        transition: all {TRANSITIONS["fast"]};
    }}

    .step-done {{
        color: {COLORS["bullish"]} !important;
    }}

    .step-active {{
        color: {COLORS["text_primary"]} !important;
        font-weight: {TYPOGRAPHY["weights"]["semibold"]};
    }}

    .step-icon {{
        font-size: 1.25rem;
        width: 1.5rem;
        text-align: center;
        flex-shrink: 0;
    }}

    .step-label {{
        flex: 1;
    }}
</style>
"""


def apply_all_styles() -> str:
    return (
        GLOBAL_STYLES
        + BUTTON_STYLES
        + NAV_STYLES
        + STOCK_LIST_STYLES
        + STOCK_HEADER_STYLES
        + INDICATORS_PANEL_STYLES
        + ANALYSIS_PANEL_STYLES
        + WAKE_SCREEN_STYLES
        + EMPTY_STATE_STYLES
        + STEP_PROGRESS_STYLES
    )
