from kink import inject
from sqlmodel import select

from app.database import AsyncEngine, AsyncSession
from app.dto.stock import UpdateStockPosition
from app.models.stock import StockPosition

__all__ = ["StockRepository"]


@inject
class StockRepository:
    __model = StockPosition

    def __init__(self, *, engine: AsyncEngine) -> None:
        self.__engine = engine

    async def create(self, stock: StockPosition) -> None:
        async with AsyncSession(self.__engine) as session:
            session.add(stock)
            await session.commit()

    async def read(self, *, symbol: str, user_id: str) -> StockPosition | None:
        statement = select(self.__model).where(
            self.__model.symbol == symbol,
            self.__model.user_id == user_id,
        )

        async with AsyncSession(self.__engine) as session:
            result = await session.exec(statement)
            return result.one_or_none()

    async def update(
        self,
        data: UpdateStockPosition,
        *,
        symbol: str,
        user_id: str,
    ) -> None:
        stock_position = await self.read(symbol=symbol, user_id=user_id)
        if stock_position is None:
            raise ValueError("Stock position not found")
        updated_stock_position = self.__model.sqlmodel_update(stock_position, data)

        async with AsyncSession(self.__engine) as session:
            session.add(updated_stock_position)
            await session.commit()

    async def delete(self, *, symbol: str, user_id: str) -> None:
        stock_position = await self.read(symbol=symbol, user_id=user_id)
        if stock_position is None:
            raise ValueError("Stock position not found")

        async with AsyncSession(self.__engine) as session:
            await session.delete(stock_position)
            await session.commit()
