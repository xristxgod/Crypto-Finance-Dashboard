from tortoise import fields

from fastapi_users.db import TortoiseBaseUserModel

from apps.common.models import AbstractIntIDModel
from apps.common.mixins import TimestampMixin

from .validators import EmailValidator, RUPhoneValidator


class User(TimestampMixin, TortoiseBaseUserModel):
    username = fields.CharField(max_length=255, unique=True)
    email = fields.CharField(index=True, unique=True, null=True, max_length=255, validators=[EmailValidator()])
    phone_number = fields.CharField(max_length=20, unique=True, null=True, validators=[RUPhoneValidator()])

    telegram = fields.ReverseRelation['Telegram']

    class Meta:
        table = "users_user"
