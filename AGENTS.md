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
│   ├── streamlit_app.py      # Main Streamlit application
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

### Streamlit App (frontend/streamlit_app.py)

**Layout:**
```
┌─────────────────────────────────────────────────────────────────────┐
│  Sidebar                                                            │
│  ───────────────                                                    │
│  Branding: "AI Equity Research" title + subtitle                   │
│  Search/filter input (filters stock list by ticker)                │
│  Stock list as styled cards (ticker, date range, signal badge)     │
│  Refresh data button                                                │
├─────────────────────────────────────────────────────────────────────┤
│  Main Page                                                          │
│  ───────────────                                                    │
│  Header: Ticker name + metadata pills (name, sector, exchange)     │
│  Stat row: Latest Close | Trading Days | Analyses Run              │
│  ───────────────                                                    │
│  Two-pane Plotly chart (dark theme):                               │
│    - Top 72%: Candlestick with range selector (1M/3M/6M/1Y/All)   │
│    - Bottom 28%: Volume bar chart (green/red colored)              │
│  ───────────────                                                    │
│  Tabs: [Analysis History] [New Analysis]                           │
│                                                                      │
│  Analysis History:                                                  │
│    - Card per analysis with left-border color (green/red/gray)     │
│    - RSI, MACD, Signal indicator blocks                             │
│    - Collapsible "View AI Thesis" expander                          │
│  New Analysis:                                                      │
│    - Period button group: 7D / 1M / 3M / 6M / 1Y / Custom         │
│    - Custom date pickers shown only when Custom selected            │
│    - Date range display pill                                        │
│    - Run Analysis button                                            │
│    - Live pipeline step progress (4 steps with icons)              │
│    - Inline result card matching history style                      │
└─────────────────────────────────────────────────────────────────────┘
```

**Key Functions:**

| Function | Cache TTL | Purpose |
|----------|-----------|---------|
| `fetch_stocks()` | 60s | Get list of ingested stocks |
| `fetch_analyses(ticker)` | 30s | Get analysis history |
| `fetch_ohlc(ticker)` | 60s | Get OHLC data for charts |
| `latest_signal(ticker)` | 30s | Get most recent signal for sidebar badge |

**Session State:**
- `backend_ready` - Whether backend responded to ping
- `ping_attempts` - Wake-up retry count
- `selected_stock` - Currently selected ticker
- `selected_period` - Active period in New Analysis tab (default: "3M")

**Backend Wake-up Logic:**
- Free-tier services sleep when idle
- Frontend polls `/ping` with a 20-second per-request timeout
- Up to 10 attempts (3-second sleep between failed attempts)
- Centered full-page wake screen with `st.progress` bar

**Chart:**
- Uses Plotly `make_subplots` with 2 rows (shared x-axis)
- Row 1 (72%): `go.Candlestick` — green up candles, red down candles
- Row 2 (28%): `go.Bar` volume — colored green/red to match candle direction
- Dark theme: `#0e1117` background, `#1f2330` grid lines
- Range selector buttons: 1M, 3M, 6M, 1Y, All
- Y-axes on the right side (finance convention)

**Theming:**
- `frontend/.streamlit/config.toml` sets `base = "dark"` so Streamlit native widgets (inputs, buttons, toolbar) render in dark mode
- Custom CSS injected via `st.markdown` overrides specific element colors to match the palette
- Both layers must be kept in sync — the config.toml values match the CSS color constants

**Color System:**
- Bullish: `#00c48c` (green) with `rgba(0,196,140,0.12)` background
- Bearish: `#ff4b4b` (red) with `rgba(255,75,75,0.12)` background
- Neutral: `#a0a0b0` (gray) with `rgba(160,160,176,0.12)` background
- App background: `#0e1117`
- Secondary background (sidebar, cards): `#13161e`
- Primary accent: `#3d5afe`

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
