from tortoise import fields

from core.common.mixins import TimestampMixin
from core.common.models import AbstractUUIDIDModel

from core.users.validators import EmailValidator, RUPhoneValidator


class User(TimestampMixin, AbstractUUIDIDModel):
    username = fields.CharField(max_length=255, unique=True)
    email = fields.CharField(index=True, unique=True, null=True, max_length=255, validators=[EmailValidator()])
    phone_number = fields.CharField(max_length=20, unique=True, null=True, validators=[RUPhoneValidator()])

    hashed_password = fields.CharField(max_length=255)

    is_active = fields.BooleanField(default=True)
    is_superuser = fields.BooleanField(default=False)
    is_verified = fields.BooleanField(default=False)

    telegram = fields.ReverseRelation['default.Telegram']
    telegram_referral_link = fields.ReverseRelation['default.TelegramReferralLink']
    accounts = fields.ReverseRelation['default.Account']

    class Meta:
        table = "users_user"
