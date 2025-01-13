from functools import lru_cache
from typing import List, Optional, Tuple, Type

from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)


class Settings(BaseSettings):
    flaresolverr_endpoint: Optional[str] = None
    flaresolverr_alt_endpoint: Optional[str] = None
    flarebypasser_endpoint: Optional[str] = None
    valkey_host: Optional[str] = "localhost"
    valkey_port: Optional[int] = 6379

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class Config(BaseSettings):
    redact_texts: List[str]

    rate_limit: Optional[bool] = False
    rate_limit_count: Optional[int] = 10
    rate_limit_duration: Optional[int] = 60  # 1 minute

    flare_use_cache: Optional[bool] = True
    flare_cache_ttl: Optional[int] = 86400  # 1 day

    model_config = SettingsConfigDict(
        extra="ignore",
        case_sensitive=False,
        yaml_file="config.yaml",
        yaml_file_encoding="utf-8",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (YamlConfigSettingsSource(settings_cls),)


@lru_cache
def get_settings():
    return Settings()


@lru_cache
def get_config():
    return Config()
