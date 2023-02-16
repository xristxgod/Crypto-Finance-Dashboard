from tortoise import fields

from fastapi_users.db import TortoiseBaseUserModel

from core.common.models import AbstractModel
from core.common.mixins import TimestampMixin


class Role(AbstractModel):
    name = fields.CharField(max_length=255)
    permissions = fields.JSONField(default=dict)

    class Meta:
        table = "users_role"


class User(TimestampMixin, TortoiseBaseUserModel):
    username = fields.CharField(max_length=255, unique=True)
    email = fields.CharField(max_length=255, unique=True)
    role_id = fields.ForeignKeyField(
        'models.Role', on_delete=fields.SET_NULL, null=True,
        related_name='users'
    )
    hashed_password = fields.CharField(max_length=255)
    is_active = fields.BooleanField(default=True)
    is_superuser = fields.BooleanField(default=False)
    is_verified = fields.BooleanField(default=False)

    class Meta:
        table = "users_user"
