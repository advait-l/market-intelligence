# Deployment Guide

This guide covers deploying both the backend (FastAPI) and frontend (Streamlit) to production.

## Prerequisites

- Python 3.10+
- Supabase account (for database)
- Render account (for hosting)
- Google Gemini API key
- GitHub account (for deployment)

## Environment Variables

Create a `.env` file with the following variables:

```
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_KEY=your_supabase_service_key
SUPABASE_DB_URL=postgresql://user:password@host:5432/dbname
GEMINI_API_KEY=your_gemini_api_key
BACKEND_URL=https://your-backend-url.onrender.com
```

## Database Setup

1. Create a new Supabase project
2. Run the SQL schema from `infra/supabase.sql` in the Supabase SQL editor
3. Get your connection string from Supabase settings

## Backend Deployment (Render)

1. Push your code to GitHub
2. Log in to [Render](https://render.com)
3. Create a new Web Service
4. Connect your GitHub repository
5. Configure:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install --no-cache-dir -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port 10000`
6. Add environment variables:
   - `SUPABASE_URL`
   - `SUPABASE_SERVICE_KEY`
   - `SUPABASE_DB_URL`
   - `GEMINI_API_KEY`
7. Deploy

**Note**: The `--no-cache-dir` flag and updated dependencies avoid the read-only filesystem issue on free tier by using pre-built wheels.

## Frontend Deployment (Render)

1. Create another Web Service on Render
2. Connect your GitHub repository
3. Configure:
   - **Root Directory**: `frontend`
   - **Build Command**: `pip install --no-cache-dir -r requirements.txt`
   - **Start Command**: `streamlit run streamlit_app.py --server.port 10000 --server.address 0.0.0.0`
4. Add environment variable:
   - `BACKEND_URL`: Your backend service URL (e.g., `https://ai-equity-research-backend.onrender.com`)
5. Deploy

**Update `streamlit_app.py`** to use the backend URL:
```python
import os
import requests

backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
# Use backend_url for API calls
```

## Local Development

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
pip install -r requirements.txt
BACKEND_URL=http://localhost:8000 streamlit run streamlit_app.py
```

## Troubleshooting

### Build fails with "Read-only file system" error
- **Cause**: Rust packages being built from source on free tier
- **Solution**: Use `--no-cache-dir` flag and ensure all dependencies use pre-built wheels (see requirements.txt)

### Backend and frontend can't communicate
- **Cause**: `BACKEND_URL` not set correctly
- **Solution**: Ensure `BACKEND_URL` environment variable is set to your backend's full URL (e.g., `https://ai-equity-research-backend.onrender.com`)

### Dependencies not found at runtime
- **Cause**: Missing environment variables or incomplete build
- **Solution**: Check build logs in Render dashboard, ensure all `SUPABASE_*` variables are set
