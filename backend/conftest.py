import pytest


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
def event_loop():
    import asyncio
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def client():
    from httpx import AsyncClient
    from src.main import app

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
async def initialize_tests():
    from tortoise import Tortoise
    from src.core import database
    from src.config import settings

    await Tortoise.init(config=settings.TEST_DATABASE_CONFIG, _create_db=True)
    await Tortoise.generate_schemas()

    yield

    await Tortoise.close_connections()
    await database.drop()


@pytest.fixture
def user_manager():
    from core.users.models import User
    from core.users.managers import UserManager, UserDatabase
    return UserManager(UserDatabase(User))
