from fastapi import APIRouter, Depends
from kink import di
from pydantic import PositiveInt

from app.api.auth import get_current_active_user_id
from app.dto.response import SimpleResponse
from app.models.stock import StockPosition
from app.services.stocks import StockService

__all__ = ["ROUTER"]

ROUTER = APIRouter(prefix="/stock")


@ROUTER.get("/{stock_symbol}")
async def get_stock(
    stock_symbol: str,
    *,
    service: StockService = Depends(lambda: di[StockService]),
    user_id: str = Depends(get_current_active_user_id),
) -> StockPosition:
    return service.get_stock_position(stock_symbol, user_id=user_id)


@ROUTER.post("/{stock_symbol}", status_code=201)
async def purchase_stock(
    stock_symbol: str,
    amount: PositiveInt,
    *,
    service: StockService = Depends(lambda: di[StockService]),
    user_id: str = Depends(get_current_active_user_id),
) -> SimpleResponse:
    await service.purchase_stock(stock_symbol, amount, user_id=user_id)

    message = f"{amount} units of stock {stock_symbol} were added to your stock record"
    return SimpleResponse(message=message)
