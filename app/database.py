"""Database config"""

import logging
from collections.abc import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from config.constants import DB_NAMING_CONVENTION
from config.settings import settings

from .json import json

DATABASE_URL = str(settings.ASYNC_DATABASE_URL)
logger = logging.getLogger(__name__)
metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)  # type: ignore
engine = AsyncEngine(
    create_engine(
        DATABASE_URL,
        echo=False,
        future=True,
        json_serializer=json.dumps,
        json_deserializer=json.loads,
        pool_size=30,
        pool_timeout=10,
    )
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async_session_maker = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )  # type: ignore
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()
