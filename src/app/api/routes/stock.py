from fastapi import APIRouter, Depends
from kink import di

from app.api.auth import get_current_active_user_id
from app.dto.response import SimpleResponse
from app.dto.stock import StockResponse
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
) -> StockResponse:
    response = await service.get_stock_position(
        stock_symbol.strip().upper(), user_id=user_id
    )
    return response


@ROUTER.post("/{stock_symbol}", status_code=201)
async def operate_stock(
    stock_symbol: str,
    amount: int,
    *,
    service: StockService = Depends(lambda: di[StockService]),
    user_id: str = Depends(get_current_active_user_id),
) -> SimpleResponse:
    await service.operate_stock(stock_symbol.strip().upper(), amount, user_id=user_id)

    message = f"{amount} units of stock {stock_symbol} were added to your stock record"
    return SimpleResponse(message=message)
