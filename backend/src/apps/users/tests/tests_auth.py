import pytest
from fastapi import status

from apps.common.factories import get_fake_user


@pytest.mark.anyio
async def test_auth(client):

    user = get_fake_user()

    response = await client.post(
        '/api/auth/register',
        json=user,
    )

    assert response.status_code == status.HTTP_201_CREATED

    response = await client.post(
        '/api/auth/login',
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        data={
            'username': user['username'],
            'password': user['password'],
        }
    )
    assert response.status_code == status.HTTP_200_OK

    cookies = response.cookies

    response = await client.post(
        '/api/auth/logout',
        cookies=cookies,
    )

    assert response.status_code == status.HTTP_200_OK
