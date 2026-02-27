from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Equity Research Agent"
    env: str = "dev"
    supabase_url: str = Field(..., alias="SUPABASE_URL")
    supabase_service_key: str = Field(..., alias="SUPABASE_SERVICE_KEY")
    supabase_db_url: str = Field(..., alias="SUPABASE_DB_URL")
    gemini_api_key: str = Field(..., alias="GEMINI_API_KEY")
    gemini_model: str = "gemini-2.5-flash"
    gemini_embedding_model: str = "models/gemini-embedding-001"
    backend_url: str = "http://localhost:8000"

    gemini_text_models: list[str] = [
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
        "gemini-1.5-flash",
        "gemini-2.5-pro",
    ]
    gemini_embedding_models: list[str] = [
        "models/gemini-embedding-001",
        "models/text-embedding-004",
    ]
    gemini_max_retries: int = 3
    gemini_retry_base_delay: float = 1.0

    model_config = SettingsConfigDict(populate_by_name=True, env_file="../.env")


settings = Settings()
