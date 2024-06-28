from urllib.parse import urljoin
from requests_html import HTMLSession
from kink import inject

from app.config import MarketWatchConfig

__all__ = ["MarketWatchGateway"]


@inject
class MarketWatchGateway:
    def __init__(self, config: MarketWatchConfig):
        self.__config = config

    async def __get_page_html(self, symbol: str) -> str:
        url = urljoin(self.__config.url, f"/investing/stock/{symbol}")
        session = HTMLSession()
        response = session.get(url)
        response.html.render()
        return response.text

    async def get_stock_performance(self, symbol: str) -> float:
        html = self.__get_page_html(symbol)
