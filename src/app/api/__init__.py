from contextlib import asynccontextmanager

from fastapi import FastAPI
from kink import di

from app.api.routes import stock
from app.database import create_all_tables

__all__ = ["APP"]


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    await create_all_tables(di)


APP = FastAPI(lifespan=lifespan)
APP.include_router(stock.ROUTER)
