from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    flaresolverr_endpoint: Optional[str] = None
    flaresolverr_alt_endpoint: Optional[str] = None
    flarebypasser_endpoint: Optional[str] = None
    host_ip: Optional[str] = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class Config(BaseSettings):
    replace_host_ip: Optional[bool] = True
    rate_limit: Optional[bool] = False  # TODO: implement

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="config_", case_sensitive=False, extra="ignore"
    )


@lru_cache
def get_settings():
    return Settings()


@lru_cache
def get_config():
    return Config()
