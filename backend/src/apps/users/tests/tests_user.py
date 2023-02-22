# https://github.com/fastapi-users/fastapi-users/blob/master/tests/conftest.py

import pytest

from fastapi_users.password import get_password_hash

from apps.common.factories import get_fake_user
from apps.users.models import User
from apps.users.schemas import UserDB, BodyUserCreate


@pytest.mark.anyio
async def test_user_me(client):
    user_data = get_fake_user()
    password = user_data['password']
    hashed_password = get_password_hash(password)

    user = await User.create(**user_data, hashed_password=hashed_password)

    response = await client.post(
        '/api/auth/login',
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        data={
            'username': user.username,
            'password': password,
        }
    )

    cookies = response.cookies

    print(cookies)

    # response = await client.post(
    #     '/api/users/me',
    #     cookies=cookies,
    # )
    #
    # assert response.json() == (await UserDB.from_orm(user)).json()
