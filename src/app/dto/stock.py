from typing import Annotated

from pydantic import AfterValidator, Field, PositiveInt

from app.dto.base import BaseDto

__all__ = [
    "StockPerformance",
    "Stock",
    "CreateStockPosition",
    "UpdateStockPosition",
    "StockResponse",
    "StockApiResponse",
]


def __validate_amount(v: int) -> int:
    if v < 0:
        raise ValueError("Amount must be greater than or equal to 0")
    return v


AMOUNT_TYPE = Annotated[int, AfterValidator(__validate_amount)]


class StockPerformance(BaseDto):
    last_five_days: float
    last_month: float
    last_three_months: float
    year_to_date: float
    last_year: float


class Stock(BaseDto):
    after_hours: float
    close: float
    from_: str = Field(alias="from")
    high: float
    low: float
    open: float
    pre_market: float
    status: str
    symbol: str
    volume: int


class CreateStockPosition(BaseDto):
    user_id: str
    symbol: str
    amount: AMOUNT_TYPE


class UpdateStockPosition(BaseDto):
    amount: AMOUNT_TYPE


class StockResponse(CreateStockPosition, Stock):
    performance: StockPerformance
