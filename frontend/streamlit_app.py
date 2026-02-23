import json
import os
from datetime import date, timedelta

import requests
import streamlit as st


st.set_page_config(page_title="AI Equity Research Agent", layout="wide")

default_backend = os.getenv("BACKEND_URL", "http://localhost:8000")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Space Grotesk', sans-serif;
    }
    .stApp {
        background: radial-gradient(circle at 10% 20%, #f2f4f8 0%, #faf7f2 45%, #eef3f8 100%);
    }
    .hero {
        padding: 1.5rem 1.2rem;
        border-radius: 18px;
        background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(245,247,250,0.85));
        box-shadow: 0 18px 40px rgba(20, 30, 55, 0.08);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>AI Equity Research Agent</h1>
        <p>Upload EOD CSVs, compute technical signals, and generate a thesis with Gemini.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Configuration")
    backend_url = st.text_input("Backend URL", value=default_backend)
    st.markdown("Upload one CSV per ticker (e.g., `AAPL_EOD.csv`).")
    uploads = st.file_uploader("CSV files", type=["csv"], accept_multiple_files=True)
    if st.button("Ingest CSVs"):
        if not uploads:
            st.warning("Please upload at least one CSV.")
        else:
            files = [("files", (f.name, f.getvalue(), "text/csv")) for f in uploads]
            response = requests.post(f"{backend_url}/ingest", files=files, timeout=120)
            if response.ok:
                st.success("Ingestion complete.")
                st.json(response.json())
            else:
                st.error(f"Ingestion failed: {response.text}")

st.subheader("Run Analysis")
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    tickers_input = st.text_input("Tickers", value="AAPL")
with col2:
    start_date = st.date_input("Start date", value=date.today() - timedelta(days=180))
with col3:
    end_date = st.date_input("End date", value=date.today())

if st.button("Analyze"):
    tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
    payload = {
        "tickers": tickers,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
    }
    response = requests.post(
        f"{backend_url}/analyze",
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"},
        timeout=180,
    )
    if response.ok:
        data = response.json()
        for result in data.get("results", []):
            st.markdown(f"### {result['ticker']}")
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("RSI", f"{result['indicators'].get('rsi', 0):.2f}")
            col_b.metric("MACD", f"{result['indicators'].get('macd', 0):.2f}")
            col_c.metric("Signal", result["indicators"].get("signal", "neutral"))
            st.write(result["thesis"])
    else:
        st.error(f"Analysis failed: {response.text}")
