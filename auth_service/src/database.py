from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import text
import asyncio

from config import settings


class DataBase(DeclarativeBase):
    __session_factory = async_sessionmaker(
        create_async_engine(
            url=settings.DATABASE_URL,
            echo=True,
            pool_size=5,
            max_overflow=10,
        )
    )

    @classmethod
    async def get_session(cls):
        return cls.__session_factory()
