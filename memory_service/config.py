"""Settings read from the environment and .env. Model IDs are configured here and nowhere else."""

from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # model_nano / model_super / model_ultra would trip pydantic's default "model_" namespace.
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", protected_namespaces=())

    database_url: str = ""

    nebius_api_key: SecretStr = SecretStr("")
    nebius_base_url: str = "https://api.tokenfactory.nebius.com/v1/"
    model_nano: str
    model_super: str
    model_ultra: str

    token_encryption_key: SecretStr = SecretStr("")

    app_timezone: str = "Asia/Kolkata"
    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    return Settings()
