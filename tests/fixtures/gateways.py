import pytest

from app.config import PolygonConfig
from app.services.marketwatch import MarketWatchService
from app.gateways.polygon import PolygonGateway

__all__ = ["polygon_gateway", "market_watch_gateway"]


@pytest.fixture
def polygon_gateway(polygon_config: PolygonConfig) -> PolygonGateway:  # type: ignore
    yield PolygonGateway(polygon_config)


@pytest.fixture
def market_watch_gateway(polygon_gateway: PolygonGateway) -> MarketWatchService:  # type: ignore
    yield MarketWatchService(polygon_gateway)
