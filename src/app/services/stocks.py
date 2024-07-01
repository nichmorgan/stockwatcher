from fastapi.exceptions import HTTPException
from kink import inject
from requests import HTTPError

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

    async def operate_stock(
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

        updated_amount = max(stock_position.amount + amount, 0)
        if updated_amount == 0:
            await self.__repository.delete(symbol=symbol, user_id=user_id)
            return

        await self.__repository.update(
            UpdateStockPosition(amount=updated_amount),
            symbol=symbol,
            user_id=user_id,
        )

    async def get_stock_position(self, symbol: str, *, user_id: str) -> StockResponse:
        stock_position = await self.__repository.read(symbol=symbol, user_id=user_id)
        position_amount = stock_position.amount if stock_position else 0

        try:
            stock_data = self.__polygon.get_stock(symbol)
            stock_performance = self.__marketwatch.get_stock_performance(symbol)
        except HTTPError as e:
            raise self.__get_stock_error(e)

        return StockResponse(
            **stock_data.model_dump(),
            user_id=user_id,
            amount=position_amount,
            performance=stock_performance,
        )

    @staticmethod
    def __get_stock_error(e: HTTPError) -> HTTPException:
        err_data = e.response.json()
        err_status = e.response.status_code
        err_msg = "Failed to fetch stock"
        msg_keys = ["error", "message"]
        for key in msg_keys:
            if key in err_data:
                err_msg = f"{err_msg}: {err_data[key]}"
                break
        return HTTPException(status_code=err_status, detail=err_msg)
