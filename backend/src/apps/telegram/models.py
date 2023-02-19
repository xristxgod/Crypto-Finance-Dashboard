from tortoise import models, fields

from apps.common.mixins import TimestampMixin


class Telegram(TimestampMixin, models.Model):
    chat_id = fields.BigIntField(pk=True)
    username = fields.CharField(max_length=255, default=None)
    is_active = fields.BooleanField(default=True)
    user = fields.OneToOneField('crypto_dashboard.User', related_name='telegram', on_delete=fields.CASCADE)

    class Meta:
        table = "telegram_telegram"
