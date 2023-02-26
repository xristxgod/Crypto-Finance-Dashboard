from tortoise import models
from tortoise import fields
from fastapi_users_tortoise import TortoiseBaseUserAccountModelUUID

from core.common.mixins import TimestampMixin


class Language(models.Model):
    id = fields.CharField(max_length=5, unique=True, pk=True)

    class Meta:
        table = 'languages'


class User(TimestampMixin, TortoiseBaseUserAccountModelUUID):
    username = fields.CharField(max_length=255, unique=True)
    email = fields.CharField(index=True, unique=True, null=True, max_length=255, validators=[])
    phone_number = fields.CharField(max_length=20, unique=True, null=True, validators=[])

    language = fields.ForeignKeyField(
        'default.Language', default='ENG', on_delete=fields.SET_NULL, null=True,
        related_name='users_language'
    )

    telegram = fields.ReverseRelation['default.Telegram']
    telegram_referral_link = fields.ReverseRelation['default.TelegramReferralLink']
    # accounts = fields.ReverseRelation['default.Account']

    class Meta:
        table = 'users_user'


class SubModel(models.Model):
    user: User

    class Meta:
        abstract = True
