from apps.telegram.models import Message


class Messanger:

    tags = ()

    @classmethod
    async def setup(cls):
        message = Message.filter(tag__in=cls.tags)
        if await message.count() != cls.tags:
            pass

    @classmethod
    async def get(cls, tag: str, language_id: str) -> tuple:
        pass
