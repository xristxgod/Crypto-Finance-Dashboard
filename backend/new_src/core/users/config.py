from __future__ import absolute_import

from fastapi_users import FastAPIUsers
from fastapi_users.authentication.strategy import JWTStrategy
from fastapi_users.authentication.transport import CookieTransport
from fastapi_users.authentication.backend import AuthenticationBackend

from config import settings


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.AUTH_SECRET_KEY, lifetime_seconds=3500)


cookie_authentication = AuthenticationBackend(
    name='auth_cookie',
    transport=CookieTransport(
        cookie_name=settings.COOKIE_NAME,
        cookie_secure=False,
        cookie_httponly=False,
    ),
    get_strategy=get_jwt_strategy,
)

auth_users = FastAPIUsers(
    # get_user_manager,
    [cookie_authentication],
)

current_active_user = auth_users.current_user(active=True)
current_superuser = auth_users.current_user(superuser=True)
