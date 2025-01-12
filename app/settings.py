from functools import lru_cache
from typing import Optional, Tuple, Type

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
    host_ip: Optional[str] = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class Config(BaseSettings):
    replace_host_ip: Optional[bool] = True
    rate_limit: Optional[bool] = False  # TODO: implement

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
