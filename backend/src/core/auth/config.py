from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy

from .managers import get_user_manager

from models import User
from config import SECRET_AUTH
