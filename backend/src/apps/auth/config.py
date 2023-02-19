from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication

from config import settings
from apps.users import schemas
from . import managers

jwt_authentication = JWTAuthentication(
    secret=settings.SECRET_KEY_AUTH,
    lifetime_seconds=3600,
)


fastapi_users = FastAPIUsers(
    managers.get_user_manager,
    [jwt_authentication],
    schemas.BodyUser,
    schemas.BodyUserCreate,
    schemas.BodyUserUpdate,
    schemas.UserDB,
)

current_active_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(superuser=True)
