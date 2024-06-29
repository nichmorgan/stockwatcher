from datetime import datetime, timezone

from pydantic import (
    BaseModel,
    Field,
    PastDatetime,
    PositiveFloat,
    field_serializer,
    field_validator,
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
        return datetime.fromtimestamp(v / 1000, tz=timezone.utc)

    @field_serializer("date", when_used="always")
    def serialize_date(date: datetime) -> int:  # type: ignore
        return int(date.timestamp() * 1000)


class MarketStockApiResponse(BaseModel):
    results: list[MarketStockRecord]
