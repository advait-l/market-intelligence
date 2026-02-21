from __future__ import annotations

from typing import Dict

import pandas as pd

from app.services.indicators import compute_macd, compute_rsi


def run_data_analyst(state: Dict) -> Dict:
    df: pd.DataFrame = state["ohlc_df"]
    close = df["close"].astype(float)

    rsi_series = compute_rsi(close)
    macd_df = compute_macd(close)

    latest_rsi = float(rsi_series.dropna().iloc[-1]) if not rsi_series.dropna().empty else 0.0
    latest_macd = float(macd_df["macd"].dropna().iloc[-1]) if not macd_df.dropna().empty else 0.0
    latest_hist = float(macd_df["hist"].dropna().iloc[-1]) if not macd_df.dropna().empty else 0.0

    signal = "neutral"
    if latest_rsi > 60 and latest_hist > 0:
        signal = "bullish"
    elif latest_rsi < 40 and latest_hist < 0:
        signal = "bearish"

    state["indicators"] = {
        "rsi": latest_rsi,
        "macd": latest_macd,
        "hist": latest_hist,
        "signal": signal,
    }
    return state
