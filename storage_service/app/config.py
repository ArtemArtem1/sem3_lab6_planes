from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=".env",
    )

    host: str
    port: int = Field(ge=1, le=65535)
    db_path: str
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"]


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
