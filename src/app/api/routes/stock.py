from fastapi import APIRouter, Depends, Request, Response
from fastapi_cache.decorator import cache
from kink import di

from app.api.auth import get_current_active_user_id
from app.dto.response import SimpleResponse
from app.dto.stock import StockResponse
from app.services.stocks import StockService

__all__ = ["ROUTER"]

ROUTER = APIRouter(prefix="/stock", tags=["stock"])


def get_stock_key_builder(
    func,
    namespace: str = "",
    request: Request = None,
    response: Response = None,
    args: tuple = (),
    kwargs: dict = {},
) -> str:
    data = ":".join(
        [
            f"symbol={kwargs['stock_symbol']}",
            f"user_id={kwargs['user_id']}",
        ]
    )
    key = f"{__name__}#{data}"
    return key


@ROUTER.get("/{stock_symbol}")
@cache(expire=60, key_builder=get_stock_key_builder)
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
