from typing import NoReturn

from tortoise import fields, models, transactions

from config import settings
from core.common.utils import generate_code
from core.common.mixins import TimestampMixin, CreatedMixin

from core.users.models import User, SubModel


class Message(models.Model):
    """
    Telegram Message Format:
    The form of writing messages to the database.
    {
        "message": "message text",
        "inline_button": [
            {
              "text": "",
              "callback_data": ""
            }
        ]
    }
    """

    tag = fields.CharField(max_length=25, unique=True, pk=True)

    message_ENG = fields.JSONField(default=dict)
    message_RU = fields.JSONField(default=dict)

    @classmethod
    async def get_message(cls, tag: str, language_id: str) -> dict:
        return (await cls.get(tag=tag).values_list(f'message_{language_id}', flat=True))[0]

    class Meta:
        table = "telegram_message"


class Telegram(TimestampMixin, SubModel):
    id = fields.BigIntField(pk=True)
    username = fields.CharField(max_length=255, default=None)
    is_active = fields.BooleanField(default=True)
    user = fields.OneToOneField('default.User', related_name='telegram', on_delete=fields.CASCADE)

    @property
    def chat_id(self) -> int:
        return self.id

    async def save(self, **kwargs) -> None:
        async with transactions.in_transaction('default'):
            await super().save(**kwargs)
            await TelegramReferralLink.filter(user_id=(await self.user.first()).id).delete()

    class Meta:
        table = "telegram_telegram"


class TelegramReferralLink(CreatedMixin, SubModel):
    code = fields.CharField(pk=True, max_length=7, default=generate_code(7))
    user = fields.OneToOneField('default.User', related_name='telegram_referral_link',
                                on_delete=fields.CASCADE)

    _bot_name = settings.TELEGRAM_BOT_CONFIG['name']

    @property
    def url(self) -> str:
        return f'https://t.me/{self._bot_name}/?start={self.code}'

    @classmethod
    async def clear_code(cls, user: User) -> NoReturn:
        code = await cls.filter(user=user).first()
        if code is not None:
            await code.delete()

    class Meta:
        table = "telegram_telegram_referral_link"
