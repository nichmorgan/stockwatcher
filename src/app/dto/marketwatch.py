from datetime import datetime, timezone

from pydantic import (
    BaseModel,
    Field,
    field_validator,
    PositiveFloat,
    PastDatetime,
    PositiveInt,
)

__all__ = ["MarketStockRecord", "MarketStockApiResponse"]


class MarketStockRecord(BaseModel):
    close: PositiveFloat = Field(alias="c")
    date: PastDatetime = Field(alias="t")

    @classmethod
    @field_validator("date", mode="before")
    def parse_date(cls, v: int | datetime) -> datetime:
        if isinstance(v, datetime):
            return v
        return datetime.fromtimestamp(v / 100, tz=timezone.utc)


class MarketStockApiResponse(BaseModel):
    results: list[MarketStockRecord]
