from datetime import datetime, timezone

import pytest
from dateutil.relativedelta import relativedelta
from polyfactory.factories.pydantic_factory import ModelFactory

from app.dto import marketwatch, stock
from app.models.stock import StockPosition


@pytest.fixture
def fake_stock() -> stock.Stock:
    return ModelFactory.create_factory(stock.Stock).build()


@pytest.fixture
def fake_create_stock_position_request() -> stock.CreateStockPositionRequest:
    return ModelFactory.create_factory(stock.CreateStockPositionRequest).build()


@pytest.fixture
def fake_create_stock_position(
    fake_create_stock_position_request,
) -> stock.CreateStockPosition:
    return ModelFactory.create_factory(stock.CreateStockPosition).build(
        **fake_create_stock_position_request.model_dump(by_alias=True)
    )


@pytest.fixture
def fake_stock_position(fake_create_stock_position) -> StockPosition:
    return ModelFactory.create_factory(StockPosition).build(
        **fake_create_stock_position.model_dump(by_alias=True)
    )


@pytest.fixture
def fake_stock_performance() -> stock.StockPerformance:
    return ModelFactory.create_factory(stock.StockPerformance).build()


@pytest.fixture
def fake_market_stock_records() -> list[marketwatch.MarketStockRecord]:
    now = datetime.now(tz=timezone.utc)
    return [
        marketwatch.MarketStockRecord(c=10, t=now),
        marketwatch.MarketStockRecord(c=10, t=now - relativedelta(days=1)),
    ]


@pytest.fixture
def fake_market_stock_api_response(
    fake_market_stock_records,
) -> marketwatch.MarketStockApiResponse:
    return marketwatch.MarketStockApiResponse(results=fake_market_stock_records)
