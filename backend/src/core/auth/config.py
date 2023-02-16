from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy

from .managers import get_user_manager

from config import settings
from core.users.models import User


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.SECRET_AUTH,
        lifetime_seconds=3600,
    )


cookie_transport = CookieTransport(
    cookie_name="token",
    cookie_max_age=3600,
)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = users.current_user()