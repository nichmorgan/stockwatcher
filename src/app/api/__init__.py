from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from kink import di

from app.api.routes import stock
from app.database import create_all_tables, init_cache

__all__ = ["APP"]


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    await create_all_tables(di)
    init_cache(di)
    yield


APP = FastAPI(lifespan=lifespan)
APP.include_router(stock.ROUTER)
