import pytest

from app import database
from tests.utils import dummy_fn_factory


@pytest.fixture(autouse=True)
def mock_database(monkeypatch):
    monkeypatch.setattr(
        database, database.create_all_tables.__name__, dummy_fn_factory()
    )
    monkeypatch.setattr(database, database.init_cache.__name__, dummy_fn_factory())
