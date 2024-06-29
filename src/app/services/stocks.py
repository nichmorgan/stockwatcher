from kink import inject

from app.dto.stock import StockResponse, UpdateStockPosition
from app.gateways.polygon import PolygonGateway
from app.models.stock import StockPosition
from app.repositories.stocks import StockRepository
from app.services.marketwatch import MarketWatchService


@inject
class StockService:
    def __init__(
        self,
        *,
        repository: StockRepository,
        marketwatch: MarketWatchService,
        polygon: PolygonGateway,
    ) -> None:
        self.__repository = repository
        self.__marketwatch = marketwatch
        self.__polygon = polygon

    async def purchase_stock(
        self,
        symbol: str,
        amount: int,
        *,
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

    async def get_stock_position(self, symbol: str, *, user_id: str) -> StockResponse:
        stock_position = await self.__repository.read(symbol=symbol, user_id=user_id)
        position_amount = stock_position.amount if stock_position else 0

        stock_data = self.__polygon.get_stock(symbol)
        stock_performance = self.__marketwatch.get_stock_performance(symbol)

        return StockResponse(
            **stock_data.model_dump(),
            user_id=user_id,
            amount=position_amount,
            performance=stock_performance,
        )
