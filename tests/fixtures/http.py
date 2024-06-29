from fastapi.testclient import TestClient
import jwt
import pytest

from app.api import APP
from app.api.auth import ALGORITHM


@pytest.fixture
def http_client(
    mock_stock_repository,
    mock_database,
) -> TestClient:  # type: ignore
    return TestClient(APP)


@pytest.fixture
def token() -> str:
    return jwt.encode({"sub": "user_id"}, "", ALGORITHM)
