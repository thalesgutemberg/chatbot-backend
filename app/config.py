"""Application configuration using pydantic-settings."""

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Environment
    environment: Literal["development", "staging", "production"] = "development"
    debug: bool = True

    # OpenAI
    openai_api_key: str = ""
    openai_model: str = "gpt-4o"

    # Tavily (Web Search)
    tavily_api_key: str = ""

    # CORS
    cors_origins: list[str] = ["*"]

    # API
    api_v1_prefix: str = "/api/v1"
    project_name: str = "UNINASSAU Customer Service API"

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.environment == "development"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
