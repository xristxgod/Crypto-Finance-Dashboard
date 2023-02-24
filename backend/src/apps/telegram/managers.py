from apps.common.managers import BaseManager

from apps.telegram.schemas import TelegramDB, BodyTelegram

__all__ = (
    'TelegramManager',
)


class TelegramManager(BaseManager[BodyTelegram, TelegramDB]):
    db_model = TelegramDB
