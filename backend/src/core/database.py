import typing

from tortoise import Tortoise

from config import settings


async def connect(
        config: dict = settings.LOCAL_DATABASE_PATH,
        generate_schemas: bool = True,
        create_db: bool = False
) -> typing.NoReturn:
    await Tortoise.init(
        **config,
        _create_db=create_db
    )
    if generate_schemas:
        await Tortoise.generate_schemas()


async def close() -> typing.NoReturn:
    await Tortoise.close_connections()


async def drop() -> typing.NoReturn:
    await Tortoise._drop_databases()
