import logging
from kink import Container, di
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import make_url

from app.config import DatabaseConfig
from app.models import *

__all__ = ["create_all_tables", "AsyncSession", "AsyncEngine"]

LOGGER = logging.getLogger(__name__)


def __create_engine(container: Container) -> AsyncEngine:
    config = container[DatabaseConfig]
    url = make_url(config.url)
    return create_async_engine(url, echo=config.echo)


di[AsyncEngine] = lambda container: __create_engine(container)


async def create_all_tables(container: Container) -> None:
    engine = __create_engine(container)
    async with engine.begin() as conn:
        LOGGER.info("Creating tables")
        await conn.run_sync(SQLModel.metadata.create_all)
        LOGGER.info("Tables created")
