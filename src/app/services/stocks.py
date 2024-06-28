from kink import inject

from app.dto.stock import StockResponse, UpdateStockPosition
from app.gateways.polygon import PolygonGateway
from app.models.stock import StockPosition
from app.repositories.stocks import StockRepository


@inject
class StockService:
    def __init__(
        self,
        *,
        repository: StockRepository,
        polygon: PolygonGateway,
    ) -> None:
        self.__repository = repository
        self.__polygon = polygon

    async def purchase_stock(
        self,
        amount: int,
        *,
        symbol: str,
        user_id: str,
    ) -> None:
        stock_position = await self.__repository.read(symbol=symbol, user_id=user_id)

        if stock_position is None:
            await self.__repository.create(
                StockPosition(symbol=symbol, user_id=user_id, amount=amount)
            )
            return

        updated_amount = stock_position.amount + amount
        await self.__repository.update(
            UpdateStockPosition(amount=updated_amount),
            symbol=symbol,
            user_id=user_id,
        )

    async def get_stock_position(self, *, symbol: str, user_id: str) -> StockResponse:
        stock_position = await self.__repository.read(symbol=symbol, user_id=user_id)
        stock_data = await self.__polygon.get_stock(symbol)
