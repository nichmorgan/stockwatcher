from kink import Container, di
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.config import DatabaseConfig
from app.models import *

__all__ = ["create_all_tables", "AsyncSession", "AsyncEngine"]


def __create_engine(container: Container) -> AsyncEngine:
    config = container[DatabaseConfig]
    return create_async_engine(
        config.url.unicode_string(),
        echo=config.echo,
    )


di[AsyncSession] = __create_engine


async def create_all_tables(container: Container) -> None:
    engine = __create_engine(container)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
