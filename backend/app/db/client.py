import psycopg
from pgvector.psycopg import register_vector
from supabase import Client, create_client

from app.core.config import settings


def get_supabase_client() -> Client:
    return create_client(settings.supabase_url, settings.supabase_service_key)


def get_pg_connection() -> psycopg.Connection:
    conn = psycopg.connect(settings.supabase_db_url)
    register_vector(conn)
    return conn
