import pytest
from kink import di

from app.config import PolygonConfig
from app.gateways.polygon import PolygonGateway
from app.services.marketwatch import MarketWatchService

__all__ = ["polygon_gateway", "market_watch_gateway"]


@pytest.fixture
def polygon_gateway(polygon_config: PolygonConfig) -> PolygonGateway:  # type: ignore
    gateway = PolygonGateway(polygon_config)
    di[PolygonGateway] = gateway
    return gateway


@pytest.fixture
def market_watch_gateway(polygon_gateway: PolygonGateway) -> MarketWatchService:  # type: ignore
    service = MarketWatchService(polygon_gateway)
    di[MarketWatchService] = service
    return service
