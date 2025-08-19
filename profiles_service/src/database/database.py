from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import settings
from database.ORM_models import Base
from logger import Logger


async_engine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=False,
)

async_session_factory = async_sessionmaker(async_engine)


async def delete_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        Logger.info(f"Tables deleted")


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        Logger.info(f"Tables created")
