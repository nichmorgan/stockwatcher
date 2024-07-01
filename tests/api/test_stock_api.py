import pytest

from app.dto.stock import Stock


@pytest.fixture(autouse=True)
def setup(mock_polygon_api): ...


def test_read_stock(http_client, fake_stock, token):
    response = http_client.get(
        f"stock/{fake_stock.symbol}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )
    assert response.status_code == 200

    response_data = Stock.model_validate(response.json())
    assert response_data == fake_stock


def test_operate_stock(
    http_client,
    fake_stock,
    fake_create_stock_position_request,
    token,
):
    data = fake_create_stock_position_request.model_dump(by_alias=True)
    response = http_client.post(
        f"stock/{fake_stock.symbol}",
        json=data,
        headers={
            "Authorization": f"Bearer {token}",
        },
    )
    assert response.status_code == 201
