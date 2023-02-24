from typing import Optional, cast

from fastapi.requests import Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users.exceptions import UserNotExists
from fastapi_users import models, password
from fastapi_users.db import BaseUserDatabase
from tortoise.contrib.pydantic.base import PydanticModel
from fastapi_users.manager import BaseUserManager

from config import settings


class UserDatabase(BaseUserDatabase):
    pass
