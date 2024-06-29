from kink import di
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["DatabaseConfig", "PolygonConfig", "CacheConfig"]


class PolygonConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="POLYGON_")

    url: str
    token: SecretStr


class DatabaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DATABASE_")

    url: str
    echo: bool = False


class CacheConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CACHE_")

    url: str
    prefix: str = "fastapi-cache"


di[PolygonConfig] = lambda _: PolygonConfig()  # type: ignore
di[DatabaseConfig] = lambda _: DatabaseConfig()  # type: ignore
di[CacheConfig] = lambda _: CacheConfig()  # type: ignore
