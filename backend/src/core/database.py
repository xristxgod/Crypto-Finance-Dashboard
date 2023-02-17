import typing

import fastapi
from tortoise.contrib.fastapi import register_tortoise

from config import settings


def connect(
        app: fastapi.FastAPI,
        config: dict = settings.DATABASE_CONFIG,
) -> typing.NoReturn:
    register_tortoise(
        app=app,
        config=config,
        generate_schemas=True,
        add_exception_handlers=True,
    )


async def drop() -> typing.NoReturn:
    from tortoise import Tortoise
    await Tortoise._drop_databases()
