from datetime import date, datetime
from enum import Enum
import logging
from urllib.parse import urljoin

from dateutil.relativedelta import relativedelta
from kink import inject
import requests

from app.config import PolygonConfig
from app.dto.marketwatch import MarketStockApiResponse, MarketStockRecord
from app.dto.stock import Stock

__all__ = ["PolygonGateway", "TimeFrame"]


class TimeFrame(str, Enum):
    Daily = "day"
    Monthly = "month"
    Quarterly = "quarter"
    Yearly = "year"


@inject
class PolygonGateway:
    __logger = logging.getLogger(__name__)

    def __init__(self, config: PolygonConfig) -> None:
        self.__config = config
        self.__params = {
            "adjusted": "true",
            "apiKey": self.__config.token.get_secret_value(),
        }

    def get_last_close_price(self, symbol: str) -> MarketStockRecord:
        url = urljoin(self.__config.url, f"/v2/aggs/ticker/{symbol}/prev")
        response = requests.get(url, params=self.__params)
        try:
            response.raise_for_status()
        except (Exception,) as e:
            self.__logger.error(f" get_stock Error {e}: {response.text}")
            raise e
        data_s = response.text
        data = MarketStockApiResponse.model_validate_json(data_s)
        if not data.results:
            raise ValueError(f"Symbol {symbol} not found")
        return data.results[0]

    def get_stock(self, symbol: str) -> Stock:
        date_s_list = list(
            map(lambda d: (date.today() - relativedelta(days=d)).isoformat(), range(3))
        )
        for date_s in date_s_list:
            url = urljoin(self.__config.url, f"/v1/open-close/{symbol}/{date_s}")
            response = requests.get(url, params=self.__params)
            try:
                response.raise_for_status()
            except requests.HTTPError as e:
                if e.response.status_code == 403:
                    continue
                raise e
            data = Stock.model_validate_json(response.text)
            return data

        raise Exception(f"Not able to get stock data for {symbol}")

    def __get_step(
        self, start_date: date, end_date: date, time_frame: TimeFrame
    ) -> int:
        step_fn_map = {
            TimeFrame.Daily: lambda: (end_date - start_date).days,
            TimeFrame.Monthly: lambda: relativedelta(end_date, start_date).months,
            TimeFrame.Quarterly: lambda: relativedelta(end_date, start_date).months
            // 3,
            TimeFrame.Yearly: lambda: relativedelta(end_date, start_date).years,
        }
        step_fn = step_fn_map.get(time_frame)
        if not step_fn:
            raise ValueError(f"Invalid time frame: {time_frame}")
        step = abs(step_fn()) - 1
        step = max(step, 1)
        return step

    def get_stock_aggregates(
        self,
        symbol: str,
        *,
        start_date: date,
        end_date: date,
        time_frame: TimeFrame,
        step: int | None = None,
        limit: int = 366,
    ) -> list[MarketStockRecord]:
        if step is None:
            step = self.__get_step(start_date, end_date, time_frame)

        url = urljoin(
            self.__config.url,
            f"/v2/aggs/ticker/{symbol}/range/{step}/{time_frame.value}/{start_date.isoformat()}/{end_date.isoformat()}",
        )
        params = {
            "adjusted": "true",
            "apiKey": self.__config.token.get_secret_value(),
            "sort": "desc",
            "limit": str(limit),
        }
        response = requests.get(url, params=params)
        try:
            response.raise_for_status()
        except (Exception,) as e:
            self.__logger.error(f"get_stock_aggregates Error {e}: {response.text}")
            raise e

        data_s = response.text
        data = MarketStockApiResponse.model_validate_json(data_s)
        return data.results
