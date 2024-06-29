from datetime import datetime, timezone
import pytest
from polyfactory.factories.pydantic_factory import ModelFactory
from dateutil.relativedelta import relativedelta

from app.dto import stock
from app.dto import marketwatch


@pytest.fixture
def fake_stock() -> stock.Stock:
    return ModelFactory.create_factory(stock.Stock).build()


@pytest.fixture
def fake_create_stock_position() -> stock.CreateStockPosition:
    return ModelFactory.create_factory(stock.CreateStockPosition).build()


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
