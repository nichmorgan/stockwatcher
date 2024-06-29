import pytest

from app.repositories.stocks import StockRepository
from tests.utils import dummy_fn_factory


@pytest.fixture
def mock_stock_repository(monkeypatch, fake_stock_position):
    monkeypatch.setattr(
        StockRepository, StockRepository.create.__name__, dummy_fn_factory(sync=False)
    )
    monkeypatch.setattr(
        StockRepository,
        StockRepository.read.__name__,
        dummy_fn_factory(fake_stock_position, sync=False),
    )
    monkeypatch.setattr(
        StockRepository,
        StockRepository.update.__name__,
        dummy_fn_factory(sync=False),
    )
    monkeypatch.setattr(
        StockRepository,
        StockRepository.delete.__name__,
        dummy_fn_factory(sync=False),
    )
