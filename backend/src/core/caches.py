from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis

from config import settings


async def connect(url: str = settings.REDIS_URL):
    redis = aioredis.from_url(
        url,
        encoding="utf8",
        decode_responses=True
    )
    FastAPICache.init(
        RedisBackend(redis),
        prefix="fastapi-cache"
    )
