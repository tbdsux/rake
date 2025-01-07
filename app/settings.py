from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    flaresolverr_endpoint: Optional[str] = None
    flaresolverr_alt_endpoint: Optional[str] = None
    flarebypasser_endpoint: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return Settings()
