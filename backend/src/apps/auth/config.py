from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieAuthentication, JWTAuthentication

from config import settings
from apps.users import schemas
from . import managers

cookie_authentication = CookieAuthentication(
    secret=settings.SECRET_KEY_AUTH,
    cookie_secure=False,
    cookie_httponly=False,
)

jwt_authentication = JWTAuthentication(
    secret=settings.SECRET_KEY_AUTH,
    lifetime_seconds=3600,
)


fastapi_users = FastAPIUsers(
    managers.get_user_manager,
    (
        # Cookie
        cookie_authentication,
        # JWT
        jwt_authentication,
    ),
    schemas.BodyUser,
    schemas.BodyUserCreate,
    schemas.BodyUserUpdate,
    schemas.UserDB,
)

get_current_active_user = fastapi_users.current_user(active=True)
get_current_superuser = fastapi_users.current_user(superuser=True)
