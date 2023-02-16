from typing import AsyncGenerator

from sqlalchemy.schema import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import functools
from src.config import settings


Base = declarative_base()

engine = create_async_engine(settings.DATABASE_URL)

metadata = MetaData(settings.DATABASE_INDEXES_NAMING_CONVENTION)


@functools.lru_cache()
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with sessionmaker(engine, class_=AsyncSession, expire_on_commit=False) as session:
        yield session
