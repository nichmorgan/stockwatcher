import re
import pytest
import requests_mock
from app.gateways.polygon import PolygonGateway
from dateutil.relativedelta import relativedelta
from tests.utils import dummy_fn_factory


@pytest.fixture
def mock_polygon(monkeypatch, fake_stock, fake_market_stock_records):
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
def mock_polygon_api(
    requests_mock: requests_mock.Mocker,
    polygon_config,
    fake_stock,
    fake_market_stock_api_response,
):
    symbol = fake_stock.symbol
    date_s = fake_market_stock_api_response.results[0].date.date().isoformat()
    from_date_s = (
        (fake_market_stock_api_response.results[0].date - relativedelta(years=1))
        .date()
        .isoformat()
    )
    token = polygon_config.token.get_secret_value()

    requests_mock.get(
        f"{polygon_config.url}/v2/aggs/ticker/{symbol}/prev\?.*",
        json=fake_market_stock_api_response.model_dump(by_alias=True),
    )

    requests_mock.get(
        f"{polygon_config.url}/v1/open-close/{symbol}/{date_s}?adjusted=true&apiKey={token}",
        json=fake_stock.model_dump(by_alias=True),
    )

    response = fake_market_stock_api_response.model_dump_json(by_alias=True)
    requests_mock.get(
        f"https://dummy.com/v2/aggs/ticker/{symbol}/range/1/day/{from_date_s}/{date_s}?adjusted=true&apiKey={token}&sort=desc&limit=366",
        text=response,
    )
