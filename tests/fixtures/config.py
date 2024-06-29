from kink import di
from pydantic import SecretStr
import pytest

from app.config import PolygonConfig

__all__ = ["polygon_config"]


@pytest.fixture
def polygon_config() -> PolygonConfig:
    config = PolygonConfig(url="https://dummy.com", token=SecretStr("dummy"))
    di[PolygonConfig] = config
    return config
