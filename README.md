# AI Equity Research Agent

Production-grade, multi-agent stock analyst that ingests EOD OHLC CSVs, computes technical indicators, and generates an investment thesis with Gemini. Built on FastAPI, LangGraph, Supabase, and Streamlit.

## Architecture
- FastAPI orchestrates ingestion and analysis
- LangGraph coordinates Data Analyst, Researcher, and Reporter agents
- Supabase stores OHLC data, analyses, and vector embeddings via pgvector
- Streamlit provides a lightweight UI

## Local Setup

### Prerequisites
- [uv](https://docs.astral.sh/uv/) installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`)

### Setup
1. Install dependencies (from project root):
   ```bash
   uv sync
   ```

2. Set environment variables (see `.env.example`).

### Backend
Run the API:
```bash
cd backend && uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
Run Streamlit:
```bash
cd frontend && uv run streamlit run streamlit_app.py
```

## Supabase
- Apply schema in `infra/supabase.sql`.
- Enable pgvector extension.

## CSV Format
Expected columns: `Date,Open,High,Low,Close,Volume` with `YYYY-MM-DD` dates.
Ticker is inferred from filename (e.g., `AAPL_EOD.csv`).

## Deployment (Free Tier)
- Backend: Render (see `infra/render.yaml`)
- Database: Supabase (Free Tier)
- UI: Streamlit Community Cloud
