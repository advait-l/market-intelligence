import pandas as pd

from app.services.indicators import compute_macd, compute_rsi


def test_indicators_compute():
    close = pd.Series([10, 10.5, 11, 10.8, 11.2, 11.5, 11.7, 12, 11.9, 12.2])
    rsi = compute_rsi(close)
    macd = compute_macd(close)
    assert len(rsi) == len(close)
    assert len(macd) == len(close)
