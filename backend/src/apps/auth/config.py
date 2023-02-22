from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieAuthentication

from config import settings
from apps.users import schemas, managers

cookie_authentication = CookieAuthentication(
    secret=settings.SECRET_KEY_AUTH,
    cookie_secure=False,
    cookie_httponly=False,
)


fastapi_users = FastAPIUsers(
    managers.get_user_manager,
    [cookie_authentication],
    schemas.BodyUser,
    schemas.BodyUserCreate,
    schemas.BodyUserUpdate,
    schemas.UserDB,
)

current_active_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(superuser=True)
