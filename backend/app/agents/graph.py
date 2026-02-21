from __future__ import annotations

from typing import Dict, TypedDict

from langgraph.graph import END, StateGraph

from app.agents.data_analyst import run_data_analyst
from app.agents.reporter import run_reporter_agent
from app.agents.researcher import run_research_agent
from app.agents.tools import fetch_ohlc, fetch_stock_id, store_analysis, store_embedding
from app.db.client import get_pg_connection, get_supabase_client


class AnalystState(TypedDict):
    ticker: str
    start_date: str
    end_date: str
    stock_id: str
    ohlc_df: object
    indicators: Dict
    research_summary: str
    final_report: str
    analysis_id: str


def ingest_or_fetch_data(state: AnalystState) -> AnalystState:
    supabase = get_supabase_client()
    stock_id = fetch_stock_id(supabase, state["ticker"])
    if not stock_id:
        raise ValueError(f"Unknown ticker: {state['ticker']}")

    df = fetch_ohlc(supabase, stock_id, state["start_date"], state["end_date"])
    if df.empty:
        raise ValueError("No OHLC data found for the date range")

    state["ohlc_df"] = df
    state["stock_id"] = stock_id
    return state


def store_results(state: AnalystState) -> AnalystState:
    supabase = get_supabase_client()
    analysis = store_analysis(
        supabase,
        state["stock_id"],
        state["start_date"],
        state["end_date"],
        state["indicators"]["rsi"],
        state["indicators"]["macd"],
        state["indicators"]["signal"],
        state["final_report"],
    )
    state["analysis_id"] = analysis["id"]

    pg_conn = get_pg_connection()
    try:
        store_embedding(pg_conn, analysis["id"], state["final_report"])
    finally:
        pg_conn.close()

    return state


def build_graph():
    graph = StateGraph(AnalystState)
    graph.add_node("ingest_or_fetch_data", ingest_or_fetch_data)
    graph.add_node("data_analyst", run_data_analyst)
    graph.add_node("research", run_research_agent)
    graph.add_node("reporter", run_reporter_agent)
    graph.add_node("store_results", store_results)

    graph.set_entry_point("ingest_or_fetch_data")
    graph.add_edge("ingest_or_fetch_data", "data_analyst")
    graph.add_edge("data_analyst", "research")
    graph.add_edge("research", "reporter")
    graph.add_edge("reporter", "store_results")
    graph.add_edge("store_results", END)

    return graph.compile()


def run_graph(initial_state: Dict) -> Dict:
    app = build_graph()
    return app.invoke(initial_state)
