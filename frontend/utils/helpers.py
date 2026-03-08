from typing import Any

from styles.theme import COLORS


def get_signal_color(signal: str) -> tuple[str, str]:
    signal_lower = signal.lower() if signal else "neutral"
    color_map = {
        "bullish": (COLORS["bullish"], COLORS["bullish_bg"]),
        "bearish": (COLORS["bearish"], COLORS["bearish_bg"]),
        "neutral": (COLORS["neutral"], COLORS["neutral_bg"]),
    }
    return color_map.get(signal_lower, color_map["neutral"])


def format_price(price: float | None) -> str:
    if price is None:
        return "—"
    return f"${price:,.2f}"


def format_percentage(value: float | None) -> str:
    if value is None:
        return "—"
    sign = "+" if value > 0 else ""
    return f"{sign}{value:.2f}%"


def get_latest_signal(analyses: list[dict[str, Any]]) -> str:
    if analyses and len(analyses) > 0:
        return analyses[0].get("signal", "neutral").lower()
    return "neutral"


def calculate_price_change(ohlc_data: list[dict[str, Any]]) -> tuple[float | None, float | None]:
    if not ohlc_data or len(ohlc_data) < 2:
        return None, None

    latest_close = ohlc_data[-1].get("close")
    previous_close = ohlc_data[-2].get("close")

    if latest_close is None or previous_close is None:
        return None, None

    change = latest_close - previous_close
    change_pct = (change / previous_close) * 100 if previous_close != 0 else 0

    return change, change_pct


def truncate_text(text: str, max_length: int = 100) -> str:
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(" ", 1)[0] + "..."


def safe_get(data: dict[str, Any], key: str, default: Any = None) -> Any:
    return data.get(key, default) if data else default
