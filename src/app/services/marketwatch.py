import logging
from datetime import date, datetime, timezone

from dateutil.relativedelta import relativedelta
from kink import inject

from app.dto.marketwatch import MarketStockRecord
from app.dto.stock import StockPerformance
from app.gateways.polygon import PolygonGateway, TimeFrame

__all__ = ["MarketWatchService"]


@inject
class MarketWatchService:
    __logger = logging.getLogger(__name__)

    def __init__(self, gateway: PolygonGateway):
        self.__gateway = gateway

    def __get_one_year_records(self, symbol: str) -> list[MarketStockRecord]:
        return self.__gateway.get_stock_aggregates(
            symbol,
            start_date=date.today() - relativedelta(years=1),
            end_date=date.today(),
            step=1,
            time_frame=TimeFrame.Daily,
        )

    @staticmethod
    def __get_time_performance(
        records: list[MarketStockRecord], delta: relativedelta | datetime
    ) -> float:
        if not records:
            return 0

        end_date = records[0].date
        if isinstance(delta, datetime):
            start_date = delta
        else:
            start_date = end_date - delta

        start_idx = (end_date - start_date).days
        if start_idx >= len(records):
            start_idx = len(records) - 1

        # TODO: Search for best date if date dont match
        while True:
            record_date = records[start_idx].date
            if record_date < start_date:
                start_idx -= 1
                continue
            break

        start_price = records[start_idx].close
        end_price = records[0].close

        performance = (end_price - start_price) / start_price
        return performance

    def get_stock_performance(self, symbol: str) -> StockPerformance:
        self.__logger.info(f"Getting one year of records for {symbol}")
        year_records = self.__get_one_year_records(symbol)
        self.__logger.info(f"Got {len(year_records)} records for {symbol}")

        last_five_days = self.__get_time_performance(
            year_records, relativedelta(days=5)
        )
        last_month = self.__get_time_performance(year_records, relativedelta(months=1))
        last_three_months = self.__get_time_performance(
            year_records, relativedelta(months=3)
        )
        year_to_date = self.__get_time_performance(year_records, relativedelta(years=1))
        last_year = self.__get_time_performance(
            year_records,
            datetime(year=datetime.now().year, month=1, day=1, tzinfo=timezone.utc),
        )

        return StockPerformance(
            last_five_days=last_five_days,
            last_month=last_month,
            last_three_months=last_three_months,
            year_to_date=year_to_date,
            last_year=last_year,
        )
