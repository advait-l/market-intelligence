# AI Equity Research Agent - Architecture Reference

> **IMPORTANT FOR AI AGENTS:** When making changes to this codebase, you MUST update this file to reflect:
> - New API endpoints
> - Changes to agent pipeline (graph.py)
> - New database tables or schema changes
> - New frontend features or UI changes
> - Changes to configuration or environment variables
> - New dependencies
>
> Before finalizing any coding task, ask yourself: "Does AGENTS.md need to be updated?"

This document provides a comprehensive overview of the codebase for AI agents working on this project.

## Project Overview

Production-grade, multi-agent stock analyst that ingests EOD OHLC CSVs, computes technical indicators, and generates investment thesis using Gemini. Built with FastAPI, LangGraph, Supabase (PostgreSQL + pgvector), and Streamlit.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERACTION                            │
├─────────────────────────────────────────────────────────────────────┤
│  Streamlit Frontend  ◄───────────────────────────────────────────┐  │
│  (frontend/streamlit_app.py)                                     │  │
│    - Display OHLC candlestick charts                             │  │
│    - Show analysis history per stock                              │  │
│    - Trigger new analysis runs                                    │  │
│    - Ingest CSV files (via backend API)                           │  │
└──────────────────────────────────────────────┬──────────────────┬─┘
                                               │                  │
                                               ▼                  │
┌─────────────────────────────────────────────────────────────────────┐
│                         FASTAPI BACKEND                              │
├─────────────────────────────────────────────────────────────────────┤
│  API Routes (backend/app/api/routes/)                               │
│    - /ping         - Health check for frontend wake-up              │
│    - /stocks       - List ingested stocks with date ranges          │
│    - /ingest       - Upload CSV files to ingest OHLC data           │
│    - /analyze      - Run multi-agent analysis pipeline              │
│    - /analyses     - Get analysis history for a ticker              │
│    - /ohlc         - Get OHLC data for charting                     │
├─────────────────────────────────────────────────────────────────────┤
│  LangGraph Multi-Agent Pipeline (backend/app/agents/)               │
│                                                                      │
│  ┌──────────────┐   ┌───────────────┐   ┌──────────────┐            │
│  │ ingest_or_   │──►│ data_analyst  │──►│ researcher   │            │
│  │ fetch_data   │   │ (indicators)  │   │ (Gemini)     │            │
│  └──────────────┘   └───────────────┘   └──────┬───────┘            │
│                                                 │                    │
│         ┌───────────────────────────────────────┘                    │
│         ▼                                                            │
│  ┌──────────────┐   ┌───────────────┐                               │
│  │ reporter     │──►│ store_results │──► Save to DB + embeddings   │
│  │ (no-op)      │   │               │                               │
│  └──────────────┘   └───────────────┘                               │
├─────────────────────────────────────────────────────────────────────┤
│  Services (backend/app/services/)                                   │
│    - gemini_client.py - Gemini API with retry & model fallback      │
│    - summarizer.py    - Text generation wrapper                      │
│    - embeddings.py    - Text embedding wrapper                       │
│    - indicators.py    - RSI/MACD technical indicator calculations   │
├─────────────────────────────────────────────────────────────────────┤
│  Ingestion (backend/app/ingestion/)                                 │
│    - csv_parser.py    - Parse CSV bytes into DataFrame              │
│    - validator.py     - Validate required columns                    │
│    - loader.py        - Load OHLC data into Supabase                │
└──────────────────────────────────────────────┬──────────────────────┘
                                               │
                                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         SUPABASE (PostgreSQL)                        │
├─────────────────────────────────────────────────────────────────────┤
│  Tables:                                                             │
│    - stocks           - Stock metadata (ticker, name, sector)        │
│    - ohlc_daily       - EOD price data (date, open, high, low, etc) │
│    - analyses         - Analysis results (RSI, MACD, signal, thesis) │
│    - analysis_embeddings - Vector embeddings via pgvector            │
└─────────────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
resume-project/
├── backend/
│   ├── app/
│   │   ├── agents/           # LangGraph multi-agent pipeline
│   │   │   ├── graph.py      # Graph definition & orchestration
│   │   │   ├── data_analyst.py   # Technical indicator computation
│   │   │   ├── researcher.py      # Gemini-powered research agent
│   │   │   ├── reporter.py       # Report formatting (no-op currently)
│   │   │   └── tools.py      # DB tools (fetch_ohlc, store_analysis, etc)
│   │   ├── api/
│   │   │   └── routes/
│   │   │       ├── ingest.py     # POST /ingest - CSV upload
│   │   │       ├── analyze.py    # POST /analyze - Run analysis
│   │   │       └── stocks.py     # GET /stocks, /analyses, /ohlc
│   │   ├── core/
│   │   │   ├── config.py     # Pydantic settings from env vars
│   │   │   └── logging.py    # Logging setup
│   │   ├── db/
│   │   │   ├── client.py     # Supabase & PostgreSQL connections
│   │   │   └── models.py    # Table name constants
│   │   ├── ingestion/
│   │   │   ├── csv_parser.py # Parse CSV bytes
│   │   │   ├── validator.py # Validate OHLC columns
│   │   │   └── loader.py    # Upsert OHLC to Supabase
│   │   ├── schemas/
│   │   │   ├── requests.py  # Pydantic request models
│   │   │   └── responses.py # Pydantic response models
│   │   ├── services/
│   │   │   ├── gemini_client.py  # Gemini API with retry logic
│   │   │   ├── summarizer.py     # Text generation wrapper
│   │   │   ├── embeddings.py     # Embedding wrapper
│   │   │   └── indicators.py     # RSI/MACD calculations
│   │   ├── utils/
│   │   │   ├── datetime.py   # Date utilities
│   │   │   └── filehash.py   # File hashing for dedup
│   │   └── main.py          # FastAPI app factory
│   ├── pyproject.toml
│   └── requirements.txt
├── frontend/
│   ├── .streamlit/
│   │   └── config.toml       # Streamlit theme configuration (dark mode)
│   ├── components/           # Modular UI components
│   │   ├── __init__.py
│   │   ├── navigation.py     # Top navigation bar
│   │   ├── stock_list.py     # Sidebar stock list
│   │   ├── stock_header.py   # Main area stock header
│   │   ├── chart_panel.py    # Candlestick + volume chart
│   │   ├── indicators_panel.py # RSI/MACD gauges (right side)
│   │   ├── analysis_panel.py  # Analysis history + run new
│   │   └── modals.py         # Loading states, errors, success displays
│   ├── styles/               # Theme and CSS
│   │   ├── __init__.py
│   │   ├── theme.py          # Color constants, design tokens
│   │   └── components.py     # Component-specific CSS
│   ├── utils/                # Utilities
│   │   ├── __init__.py
│   │   ├── api.py            # Backend API calls
│   │   └── helpers.py        # Data transformations
│   ├── streamlit_app.py      # Main app (orchestrator only)
│   ├── pyproject.toml
│   └── requirements.txt
├── infra/
│   ├── render.yaml           # Render deployment config
│   └── supabase.sql          # Database schema
├── pyproject.toml            # Root workspace config
├── README.md
├── DEPLOY.md                 # Deployment guide
└── AGENTS.md                 # This file
```

## Backend Details

### FastAPI App (backend/app/main.py)

```python
# App factory pattern
def create_app() -> FastAPI:
    app = FastAPI(title="AI Equity Research Agent")
    app.include_router(ingest_router)
    app.include_router(analyze_router)
    app.include_router(stocks_router)
    return app

app = create_app()
```

### Configuration (backend/app/core/config.py)

Environment variables (required):
- `SUPABASE_URL` - Supabase project URL
- `SUPABASE_SERVICE_KEY` - Supabase service role key
- `SUPABASE_DB_URL` - PostgreSQL connection string
- `GEMINI_API_KEY` - Google Gemini API key

Configuration:
- Gemini models: `gemini-2.5-flash` (primary), with fallbacks
- Embedding models: `models/gemini-embedding-001`
- Max retries: 3 with exponential backoff

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/ping` | Health check (used by frontend to wake backend) |
| GET | `/stocks` | List all stocks with min/max dates |
| POST | `/ingest` | Upload CSV files to ingest OHLC data |
| POST | `/analyze` | Run analysis pipeline for tickers |
| GET | `/analyses?ticker=X` | Get analysis history for a ticker |
| GET | `/ohlc?ticker=X` | Get OHLC data for charting |

### LangGraph Agent Pipeline (backend/app/agents/graph.py)

Graph flow:
```
ingest_or_fetch_data → data_analyst → researcher → reporter → store_results → END
```

**State (AnalystState TypedDict):**
- `ticker` - Stock ticker symbol
- `start_date` / `end_date` - Analysis date range
- `stock_id` - UUID from stocks table
- `ohlc_df` - Pandas DataFrame with OHLC data
- `indicators` - Dict with RSI, MACD, signal
- `research_summary` - Research notes from Gemini
- `final_report` - Investment thesis
- `analysis_id` - UUID of stored analysis

**Nodes:**

1. `ingest_or_fetch_data` - Fetch stock_id and OHLC data from DB
2. `data_analyst` - Compute RSI (14-period) and MACD (12/26/9)
3. `researcher` - Call Gemini to generate research notes and thesis
4. `reporter` - No-op (report generated in researcher)
5. `store_results` - Save analysis to DB + store embedding

### Technical Indicators (backend/app/services/indicators.py)

**RSI (Relative Strength Index):**
- Period: 14 days
- Formula: `100 - (100 / (1 + RS))` where RS = avg_gain / avg_loss

**MACD (Moving Average Convergence Divergence):**
- Fast EMA: 12 periods
- Slow EMA: 26 periods
- Signal line: 9 periods
- Histogram = MACD line - Signal line

**Signal Logic (backend/app/agents/data_analyst.py:21-25):**
```python
if latest_rsi > 60 and latest_hist > 0:
    signal = "bullish"
elif latest_rsi < 40 and latest_hist < 0:
    signal = "bearish"
else:
    signal = "neutral"
```

### Ingestion Pipeline

1. Parse CSV bytes → validate columns
2. Normalize column names (lowercase, underscores)
3. Extract ticker from filename (e.g., `AAPL_EOD.csv` → `AAPL`)
4. Upsert to `ohlc_daily` table (conflict: stock_id + date)

**Required CSV columns:** `Date, Open, High, Low, Close, Volume`
**Optional columns:** `Ticker` (if present, overrides filename)

### Gemini Client (backend/app/services/gemini_client.py)

Features:
- Automatic retry with exponential backoff
- Model fallback chain (multiple Gemini models)
- Rate limit detection (429 / RESOURCE_EXHAUSTED)
- Both text generation and embedding support

## Frontend Details

### Architecture Overview

The frontend uses a **modular, component-based architecture** with clear separation of concerns:
- **Orchestrator** (`streamlit_app.py`): Main entry point that coordinates components
- **Components** (`components/`): Self-contained UI modules
- **Styles** (`styles/`): Centralized theme and CSS management
- **Utils** (`utils/`): API calls and data transformations

### Layout Structure

```
┌─────────────────────────────────────────────────────────────────┐
│  TOP NAVIGATION BAR (60px)                                      │
│  [Logo] AI Equity Research    [Stock Selector]    [Actions]    │
├───────────┬─────────────────────────────────────────────────────┤
│           │  STOCK HEADER (80px)                                │
│  SIDEBAR  │  Ticker Name | Price | Change | Sector | Exchange   │
│  (240px)  ├─────────────────────────────────────────────────────┤
│           │  MAIN CONTENT AREA                                  │
│  [Search] │  ┌─────────────────────┬────────────────────────┐   │
│  [List]   │  │                     │                        │   │
│  AAPL     │  │   CHART PANEL       │   INDICATORS PANEL     │   │
│  MSFT     │  │   (Candlestick +    │   (RSI Gauge)          │   │
│  GOOGL    │  │    Volume)          │   (MACD Gauge)         │   │
│  ...      │  │                     │   (Signal Badge)       │   │
│           │  │                     │   [Run Analysis Btn]   │   │
│           │  └─────────────────────┴────────────────────────┘   │
│           │  ANALYSIS PANEL (Expandable)                        │
│           │  ┌───────────────────────────────────────────────┐  │
│           │  │ Analysis History (cards)                      │  │
│           │  └───────────────────────────────────────────────┘  │
└───────────┴─────────────────────────────────────────────────────┘
```

### Component Modules

**1. Navigation** (`components/navigation.py`)
- Top navigation bar with logo, stock selector, and action buttons
- Logo and branding on left
- Stock selector dropdown in center (when multiple stocks available)
- Action buttons on right

**2. Stock List** (`components/stock_list.py`)
- Sidebar with search/filter functionality
- Compact list items (no cards) with:
  - Ticker (bold)
  - Date range (small, gray)
  - Signal badge (right-aligned pill)
- Active state: left border accent + background highlight
- Refresh button at bottom

**3. Stock Header** (`components/stock_header.py`)
- Large ticker name (2.5rem, bold)
- Company name (gray)
- Metadata pills (sector, exchange)
- Stat cards row:
  - Latest Close
  - Change (absolute)
  - Change % (percentage)
  - Trading Days
  - Analyses Run

**4. Chart Panel** (`components/chart_panel.py`)
- Plotly candlestick + volume chart
- Two-row layout (72% price, 28% volume)
- Range selector buttons (1M, 3M, 6M, 1Y, All)
- Dark theme with custom colors
- Y-axes on right side

**5. Indicators Panel** (`components/indicators_panel.py`)
- RSI gauge with progress bar (0-100, color-coded zones)
- MACD gauge with histogram visualization
- Large signal badge (bullish/bearish/neutral)
- Analysis period selector (7D, 1M, 3M, 6M, 1Y, Custom)
- Date range display
- "Run Analysis" button (primary action)

**6. Analysis Panel** (`components/analysis_panel.py`)
- Header with analysis count
- Analysis cards with:
  - Date range + timestamp
  - RSI, MACD, Signal indicators (compact)
  - Left border color matching signal
  - Collapsible thesis expander

**7. Modals** (`components/modals.py`)
- Wake screen (backend startup)
- Step progress indicator (pipeline steps)
- Error state display
- Success result display

### Styling System

**Theme** (`styles/theme.py`)
- Design tokens: colors, spacing, typography, layout dimensions
- Color system:
  - Backgrounds: `#0e1117` (primary), `#13161e` (secondary), `#1a1e2e` (tertiary)
  - Text: `#e8eaf6` (primary), `#9098b8` (secondary), `#5c6180` (muted)
  - Accents: `#3d5afe` (primary blue)
  - Signals: `#00c48c` (bullish), `#ff4b4b` (bearish), `#a0a0b0` (neutral)

**Components CSS** (`styles/components.py`)
- Global styles (app, sidebar, buttons, inputs)
- Component-specific CSS classes
- Applied via `st.markdown(apply_all_styles(), unsafe_allow_html=True)`

### Utilities

**API** (`utils/api.py`)
- `fetch_stocks()` - Get all stocks (60s cache)
- `fetch_analyses(ticker)` - Get analysis history (30s cache)
- `fetch_ohlc(ticker, start, end)` - Get OHLC data (60s cache)
- `ping_backend()` - Health check for wake-up
- `run_analysis(ticker, start, end)` - Trigger analysis pipeline

**Helpers** (`utils/helpers.py`)
- `get_signal_color(signal)` - Map signal to color
- `format_price(price)` - Format with $ and commas
- `format_percentage(value)` - Format with +/-
- `get_latest_signal(analyses)` - Extract most recent signal
- `calculate_price_change(ohlc)` - Compute price change from data

### Session State

- `backend_ready` - Whether backend responded to ping
- `ping_attempts` - Wake-up retry count (max: 10)
- `selected_stock` - Currently selected ticker
- `selected_period` - Active period (default: "3M")
- `analyses_cache` - Dict of ticker → analyses list (prevents redundant fetches)

### Backend Wake-up Logic

1. On app start, check `backend_ready` flag
2. If not ready, show wake screen with progress bar
3. Poll `/ping` endpoint with 20s timeout
4. Retry up to 10 times with 3s sleep between attempts
5. On success: set `backend_ready=True` and continue
6. On failure after 10 attempts: show error message

### Chart Details

- Uses Plotly `make_subplots` with 2 rows (shared x-axis)
- Row 1 (72%): `go.Candlestick` — green up candles, red down candles
- Row 2 (28%): `go.Bar` volume — colored green/red to match candle direction
- Dark theme: `#0e1117` background, `#1f2330` grid lines
- Range selector buttons: 1M, 3M, 6M, 1Y, All
- Y-axes on the right side (finance convention)
- Hover labels with dark background

### Future Extensibility

The modular architecture enables easy additions:
- **New panels**: Add component module, import in orchestrator
- **Watchlists**: Add section to sidebar
- **Comparison view**: New component with multiple stocks
- **Alerts**: Add icon to top nav
- **Export**: Add button to analysis panel
- **Settings**: New modal/page
- **News feed**: New panel component

## Database Schema (infra/supabase.sql)

```sql
-- Stocks metadata
stocks (
    id UUID PRIMARY KEY,
    ticker TEXT UNIQUE NOT NULL,
    name TEXT,
    sector TEXT,
    exchange TEXT,
    created_at TIMESTAMP
)

-- EOD price data
ohlc_daily (
    id UUID PRIMARY KEY,
    stock_id UUID REFERENCES stocks(id),
    date DATE NOT NULL,
    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    close NUMERIC,
    volume BIGINT,
    source_file_hash TEXT,
    created_at TIMESTAMP,
    UNIQUE (stock_id, date)
)

-- Analysis results
analyses (
    id UUID PRIMARY KEY,
    stock_id UUID REFERENCES stocks(id),
    date_range_start DATE,
    date_range_end DATE,
    rsi NUMERIC,
    macd NUMERIC,
    signal TEXT,
    summary TEXT,
    created_at TIMESTAMP
)

-- Vector embeddings
analysis_embeddings (
    id UUID PRIMARY KEY,
    analysis_id UUID REFERENCES analyses(id),
    embedding VECTOR(3072),
    model TEXT,
    created_at TIMESTAMP
)
```

**Index:**
- `idx_ohlc_stock_date` on `ohlc_daily(stock_id, date)`
- `idx_analysis_stock` on `analyses(stock_id)`

## Infrastructure

### Deployment (infra/render.yaml)

Two services:
1. `ai-equity-research-backend` - FastAPI on port 10000
2. `ai-equity-research-frontend` - Streamlit on port 10000

Both use Python 3.11.8 (via `PYTHON_VERSION` env var) to ensure pre-built wheels.

### Environment Variables

**Backend:**
- `SUPABASE_URL`
- `SUPABASE_SERVICE_KEY`
- `SUPABASE_DB_URL`
- `GEMINI_API_KEY`

**Frontend:**
- `BACKEND_URL` - URL of backend service

## Common Development Tasks

### Run Locally

```bash
# Backend
cd backend && uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend
cd frontend && uv run streamlit run streamlit_app.py
```

### Run Tests

```bash
uv run pytest backend/tests/
```

### Run Linting

```bash
uv run ruff check .
uv run ruff format . --check
```

### Add Dependencies

```bash
# Add to backend
cd backend && uv add <package>

# Add to frontend
cd frontend && uv add <package>
```

## Key Patterns & Conventions

1. **Pydantic v2** for all request/response schemas
2. **Supabase Client** for REST API operations (stocks, ohlc, analyses)
3. **psycopg** directly for pgvector operations (embeddings)
4. **uv workspace** for monorepo package management
5. **Ruff** for linting (line-length: 100)
6. **No inline comments** unless requested
7. **Type hints** on all function signatures

## Error Handling

- `ValueError` for validation errors (ticker not found, no OHLC data)
- HTTP errors returned to frontend for display
- Gemini rate limits trigger retries with backoff
- Frontend shows user-friendly error messages
