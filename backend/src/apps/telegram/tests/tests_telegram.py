import json

import pytest
from fastapi import status

from core.users.tests.factories import get_fake_user
from .factories import get_fake_telegram


@pytest.mark.anyio
class TestTelegram:

    @staticmethod
    async def auth(client, user):
        response = await client.post(
            '/api/auth/login',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data={
                'username': user['username'],
                'password': user['password'],
            }
        )

        return response.cookies

    @staticmethod
    async def valid_telegram_link(client, cookies, user_id):
        from apps.telegram.models import TelegramReferralLink
        response = await client.get(
            '/api/telegram/',
            cookies=cookies
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['link'] == (await TelegramReferralLink.get(user_id=user_id)).url

    async def test_telegram(self, client, user_manager):
        from core.users.schemas import BodyCreateUser
        from apps.telegram.schemas import BodyTelegram
        from apps.telegram.models import Telegram

        user = get_fake_user()
        create_user_schema = BodyCreateUser(**user)
        user_model = await user_manager.create(create_user_schema)

        cookies = await self.auth(client, user)

        await self.valid_telegram_link(client, cookies, user_id=user_model.id)

        telegram = get_fake_telegram(user_id=user_model.id)
        telegram_model = await Telegram.create(**telegram)

        response = await client.get(
            '/api/telegram/',
            cookies=cookies
        )

        assert response.status_code == status.HTTP_200_OK
        assert json.dumps(response.json()) == BodyTelegram.from_orm(telegram_model).json()

        response = await client.delete(
            '/api/telegram/',
            cookies=cookies
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        await self.valid_telegram_link(client, cookies, user_id=user_model.id)
