from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration for OmniSight."""

    model_config = SettingsConfigDict(
        env_prefix="OMNISIGHT_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    vlm_provider: str = "rule_based"
    ollama_base_url: str = "http://127.0.0.1:11434"
    ollama_model: str = "qwen2.5vl:3b"
    github_token: str = ""
    github_repository: str = ""
    github_base_branch: str = "main"


@lru_cache
def get_settings() -> Settings:
    """Return the cached OmniSight application settings."""
    return Settings()