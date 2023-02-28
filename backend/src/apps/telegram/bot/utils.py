import functools
from typing import Callable

from apps.telegram.bot.middlewares.user_database import BaseUser, AnonymousUser


def current_user(func: Callable):
    @functools.wraps(func)
    async def wrapper(message, user: BaseUser, **kwargs):
        if isinstance(user, AnonymousUser):
            from apps.telegram.bot.messanger import messanger
            return messanger.get_message('user_not_found', user, message)
        return await func(message, user, **kwargs)
    return wrapper
