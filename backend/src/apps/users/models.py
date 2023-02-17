from tortoise import fields

from fastapi_users.db import TortoiseBaseUserModel

from apps.common.models import AbstractIntIDModel
from apps.common.mixins import TimestampMixin

from .validators import EmailValidator, RUPhoneValidator


class Role(AbstractIntIDModel):
    name = fields.CharField(max_length=255, unique=True)
    description = fields.TextField(null=True)
    permissions = fields.JSONField(default=dict)

    class Meta:
        table = "users_role"


class User(TimestampMixin, TortoiseBaseUserModel):
    username = fields.CharField(max_length=255, unique=True)
    email = fields.CharField(index=True, unique=True, null=False, max_length=255, validators=(EmailValidator(),))
    phone_number = fields.CharField(max_length=20, unique=True, null=True, validators=(RUPhoneValidator(),))
    role = fields.ForeignKeyField('crypto_dashboard.Role', on_delete=fields.SET_NULL, null=True, related_name='users')

    class Meta:
        table = "users_user"
