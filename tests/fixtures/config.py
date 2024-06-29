from pydantic import SecretStr
import pytest

from app.config import PolygonConfig

__all__ = ["polygon_config"]


@pytest.fixture
def polygon_config() -> PolygonConfig:
    return PolygonConfig(url="dummy", token=SecretStr("dummy"))
