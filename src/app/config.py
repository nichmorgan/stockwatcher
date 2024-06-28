from kink import di
from pydantic import PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["DatabaseConfig", "MarketWatchConfig", "PolygonConfig"]


class PolygonConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="STOCK_")

    url: str
    token: SecretStr


class MarketWatchConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="MARKETWATCH_")

    url: str


class DatabaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DATABASE_")

    url: PostgresDsn
    echo: bool = False


di[PolygonConfig] = lambda _: PolygonConfig()  # type: ignore
di[MarketWatchConfig] = lambda _: MarketWatchConfig()  # type: ignore
di[DatabaseConfig] = lambda _: DatabaseConfig()  # type: ignore
