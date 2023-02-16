from __future__ import absolute_import

from typing import AsyncGenerator

from sqlalchemy.schema import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import functools

try:
    from config import settings
except ModuleNotFoundError:
    from src.config import settings


engine = create_async_engine(settings.DATABASE_URL)

metadata = MetaData(settings.DATABASE_INDEXES_NAMING_CONVENTION)

Model = declarative_base(metadata=metadata)


@functools.lru_cache()
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with sessionmaker(engine, class_=AsyncSession, expire_on_commit=False) as session:
        yield session
