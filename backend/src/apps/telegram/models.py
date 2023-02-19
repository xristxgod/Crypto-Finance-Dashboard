from typing import NoReturn

from tortoise import models, fields

from config import settings
from apps.common.utils import generate_code
from apps.users.models import User
from apps.common.mixins import TimestampMixin, CreatedMixin


class Telegram(TimestampMixin, models.Model):
    chat_id = fields.BigIntField(pk=True)
    username = fields.CharField(max_length=255, default=None)
    is_active = fields.BooleanField(default=True)
    user = fields.OneToOneField('default.User', related_name='telegram', on_delete=fields.CASCADE)

    class Meta:
        table = "telegram_telegram"


class TelegramReferralLink(CreatedMixin, models.Model):
    code = fields.CharField(pk=True, max_length=7, default=generate_code(7))
    user = fields.OneToOneField('default.User', related_name='telegram_referral_link',
                                on_delete=fields.CASCADE)

    _bot_name = settings.TELEGRAM_BOT_NAME

    @property
    def url(self) -> str:
        return f'https://t.me/{self._bot_name}/?start={self.code}'

    @classmethod
    async def clear_code(cls, user: User) -> NoReturn:
        code = await cls.filter(user=user).first()
        if code is not None:
            await code.delete()

    class Meta:
        table = "telegram_telegram_refferal_link"
