# Deployment Guide

This guide covers deploying both the backend (FastAPI) and frontend (Streamlit) to production. We recommend deploying to [Render](https://render.com) and [Supabase](https://supabase.com).

## Prerequisites

- GitHub account
- Supabase account (for database)
- Render account (for hosting)
- Google Gemini API key

## Database Setup (Supabase)

1. Create a new Supabase project at [database.new](https://database.new).
2. Go to the **SQL Editor** in your Supabase dashboard.
3. Open `infra/supabase.sql` from your project and run the SQL commands to set up the schema.
4. Go to **Project Settings -> Database** and copy your Connection string (URI). Make sure to replace `[YOUR-PASSWORD]` with your actual database password. This is your `SUPABASE_DB_URL`.
5. Go to **Project Settings -> API** and copy your Project URL (`SUPABASE_URL`) and `service_role` secret (`SUPABASE_SERVICE_KEY`).

## Option 1: Automatic Deployment (Recommended)

You can deploy both the frontend and backend simultaneously using Render Blueprints.

1. Push your code to a GitHub repository.
2. Log in to [Render](https://render.com).
3. Go to the **Blueprints** tab and click **New Blueprint Instance**.
4. Connect your GitHub repository.
5. Render will automatically detect the `infra/render.yaml` file.
6. You will be prompted to enter your environment variables (`SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, `SUPABASE_DB_URL`, `GEMINI_API_KEY` for the backend, and `BACKEND_URL` for the frontend). 
   *(Note: For the frontend's `BACKEND_URL`, you can initially leave it blank or enter a placeholder, then update it after the backend service is created and has a valid URL like `https://ai-equity-research-backend.onrender.com`)*
7. Click **Apply** to deploy both services.

## Option 2: Manual Deployment

If you prefer to deploy manually, create two separate Web Services on Render.

### Backend Deployment

1. On Render, click **New +** -> **Web Service**.
2. Connect your GitHub repository.
3. Configure the service:
   - **Name**: `ai-equity-research-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Python`
   - **Build Command**: `pip install --no-cache-dir -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port 10000`
4. Expand **Advanced** and add the following Environment Variables:
   - `PYTHON_VERSION`: `3.11.8` *(Crucial to prevent build errors like `ModuleNotFoundError: No module named 'pkg_resources'`)*
   - `SUPABASE_URL`: Your Supabase URL
   - `SUPABASE_SERVICE_KEY`: Your Supabase Service Role Key
   - `SUPABASE_DB_URL`: Your PostgreSQL connection string
   - `GEMINI_API_KEY`: Your Gemini API key
5. Click **Create Web Service**.
6. Once deployed, copy the Render URL (e.g., `https://ai-equity-research-backend.onrender.com`).

### Frontend Deployment

1. On Render, click **New +** -> **Web Service**.
2. Connect your GitHub repository.
3. Configure the service:
   - **Name**: `ai-equity-research-frontend`
   - **Root Directory**: `frontend`
   - **Environment**: `Python`
   - **Build Command**: `pip install --no-cache-dir -r requirements.txt`
   - **Start Command**: `streamlit run streamlit_app.py --server.port 10000 --server.address 0.0.0.0 --server.headless true --browser.gatherUsageStats false`
4. Expand **Advanced** and add the following Environment Variables:
   - `PYTHON_VERSION`: `3.11.8`
   - `BACKEND_URL`: The URL of your backend service (e.g., `https://ai-equity-research-backend.onrender.com`)
5. Click **Create Web Service**.

## Troubleshooting

### `ModuleNotFoundError: No module named 'pkg_resources'` / pandas build failure
- **Cause**: Render is attempting to build pandas from source using a very new version of Python (like Python 3.14) which is missing setuptools.
- **Solution**: Ensure you have set the `PYTHON_VERSION` environment variable to `3.11.8` in Render. This ensures pre-built wheels can be used.

### Build fails with "Read-only file system" error
- **Cause**: Packages are being built from source on the Render Free tier, filling up disk space or accessing restricted areas.
- **Solution**: The `PYTHON_VERSION=3.11.8` variable and `--no-cache-dir` flag in the build command resolve this.

### Frontend says "Failed to connect to backend"
- **Cause**: `BACKEND_URL` is missing or incorrect.
- **Solution**: Verify the `BACKEND_URL` environment variable on the frontend service. It should be the exact URL of your backend, without a trailing slash.