import functools
from typing import Callable


def keys_validator(func: Callable):
    @functools.wraps(func)
    async def wrapper(self, public, secret):

        # TODO write keys validator by service

        return await func(self, public, secret)
    return wrapper
