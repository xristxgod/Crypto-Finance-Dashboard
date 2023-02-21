from tortoise import fields

from fastapi_users.db import TortoiseBaseUserModel

from apps.common.mixins import TimestampMixin

from .validators import EmailValidator, RUPhoneValidator


class User(TimestampMixin, TortoiseBaseUserModel):
    username = fields.CharField(max_length=255, unique=True)
    email = fields.CharField(index=True, unique=True, null=True, max_length=255, validators=[EmailValidator()])
    phone_number = fields.CharField(max_length=20, unique=True, null=True, validators=[RUPhoneValidator()])

    telegram = fields.ReverseRelation['default.Telegram']
    telegram_referral_link = fields.ReverseRelation['default.TelegramReferralLink']
    accounts = fields.ReverseRelation['default.Account']

    class Meta:
        table = "users_user"
