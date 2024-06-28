from datetime import date
from urllib.parse import urljoin

import aiohttp
from kink import inject

from app.config import PolygonConfig
from app.dto.stock import Stock

__all__ = ["PolygonGateway"]


@inject
class PolygonGateway:
    def __init__(self, config: PolygonConfig) -> None:
        self.__config = config

    async def get_stock(self, symbol: str) -> Stock:
        date_s = date.today().isoformat()
        url = urljoin(self.__config.url, f"/v1/open-close/{symbol}/{date_s}")
        params = {"adjusted": "true", "apiKey": self.__config.token.get_secret_value()}
        async with aiohttp.ClientSession() as session:
            response = await session.get(url, params=params)
            response.raise_for_status()
            return Stock.model_validate(response.json())
