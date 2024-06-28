from sqlalchemy import PrimaryKeyConstraint

from app.dto.stock import CreateStockPosition

__all__ = ["StockPosition"]


class StockPosition(CreateStockPosition, table=True):
    __table_args__ = (PrimaryKeyConstraint("user_id", "symbol"),)
