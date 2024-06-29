import pytest
from app.gateways.polygon import PolygonGateway
from tests.utils import dummy_fn_factory


@pytest.fixture
def polygon_mock(monkeypatch, fake_stock, fake_market_stock_records):
    monkeypatch.setattr(
        PolygonGateway,
        PolygonGateway.get_stock.__name__,
        dummy_fn_factory(fake_stock, sync=True),
    )
    monkeypatch.setattr(
        PolygonGateway,
        PolygonGateway.get_stock_aggregates.__name__,
        dummy_fn_factory(fake_market_stock_records, sync=True),
    )


@pytest.fixture
def polygon_api_mock(monkeypatch, fake_stock, fake_market_stock_records):
    monkeypatch.setattr(
        PolygonGateway,
        PolygonGateway.get_stock.__name__,
        dummy_fn_factory(fake_stock, sync=True),
    )
    monkeypatch.setattr(
        PolygonGateway,
        PolygonGateway.get_stock_aggregates.__name__,
        dummy_fn_factory(fake_market_stock_records, sync=True),
    )
