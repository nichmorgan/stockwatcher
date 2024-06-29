import pytest
import requests_mock


def test_read_stock(
    http_client,
    fake_stock,
    token,
    mock_polygon_api,
):
    pytest.skip("This test is not working yet")
    response = http_client.get(
        f"stock/{fake_stock.symbol}",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )
    assert response.status_code == 200


def test_operate_stock(
    http_client,
    fake_stock,
    token,
):
    pytest.skip("This test is not working yet")
    response = http_client.post(
        f"stock/{fake_stock.symbol}",
        data={"amount": 1},
        headers={
            "Authorization": f"Bearer {token}",
        },
    )
    assert response.status_code == 200
