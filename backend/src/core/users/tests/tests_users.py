import pytest
from fastapi import status

from .factories import get_fake_user


@pytest.mark.anyio
class TestUser:

    async def test_user_me(self, client, user_manager):
        from core.users.models import User
        from core.users.schemas import BodyUser, BodyCreateUser

        user = get_fake_user()
        create_user_schema = BodyCreateUser(**user)

        user_model = await user_manager.create(create_user_schema)

        response = await client.post(
            '/api/auth/login',
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data={
                'username': user['username'],
                'password': user['password'],
            }
        )

        cookies = response.cookies

        response = await client.get(
            '/api/users/me',
            cookies=cookies,
        )

        user['id'] = str(user_model.id)

        assert response.json() == BodyUser(**user).dict()

        user['email'] = 'test@mail.ru'

        response = await client.patch(
            '/api/users/me',
            json=user,
            cookies=cookies,
        )

        assert response.json()['email'] == user['email']

        response = await client.delete(
            '/api/users/me',
            cookies=cookies,
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        assert not await User.filter(id=user['id']).exists()
