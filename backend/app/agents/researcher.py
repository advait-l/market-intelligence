from __future__ import annotations

from typing import Dict

from app.services.summarizer import generate_text


def run_research_agent(state: Dict) -> Dict:
    indicators = state.get("indicators", {})
    ticker = state["ticker"]
    start_date = state["start_date"]
    end_date = state["end_date"]

    # Combined prompt for both research and final report
    prompt = (
        "You are an equity research analyst. "
        "Based on the technical indicators below, provide a comprehensive investment analysis.\n\n"
        "Format your response as:\n"
        "RESEARCH NOTES:\n"
        "[3-5 bullet points on trend strength and risks]\n\n"
        "INVESTMENT THESIS:\n"
        "[Professional thesis statement, key risks, and one-line conclusion]\n\n"
        f"Ticker: {ticker}\n"
        f"Date range: {start_date} to {end_date}\n"
        f"RSI: {indicators.get('rsi', 0):.2f}\n"
        f"MACD: {indicators.get('macd', 0):.2f}\n"
        f"Histogram: {indicators.get('hist', 0):.2f}\n"
        f"Signal: {indicators.get('signal', 'neutral')}\n"
    )

    response = generate_text(prompt)

    # Parse response into research and final report
    parts = response.split("INVESTMENT THESIS:")
    state["research_summary"] = parts[0].replace("RESEARCH NOTES:", "").strip()
    state["final_report"] = parts[1].strip() if len(parts) > 1 else response.strip()

    return state
