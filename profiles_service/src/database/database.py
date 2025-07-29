from typing import Annotated

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import settings
from ORM_models import Base


async_engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=True,
)

async_session_factory = async_sessionmaker(async_engine)


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
