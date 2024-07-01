import pytest


@pytest.fixture(autouse=True)
def setup(mock_polygon): ...


def test_get_stock_performance(
    market_watch_gateway,
    fake_market_stock_records,
    fake_stock,
):
    performance = market_watch_gateway.get_stock_performance(fake_stock.symbol)

    expected_performance = (
        fake_market_stock_records[-1].close - fake_market_stock_records[0].close
    ) / fake_market_stock_records[0].close

    assert all(
        map(lambda v: v == expected_performance, performance.model_dump().values())
    )
