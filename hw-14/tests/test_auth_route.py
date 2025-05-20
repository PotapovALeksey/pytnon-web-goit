from unittest.mock import MagicMock

from starlette import status

from src.config.constants import APIRoutes, Messages

AUTH_ROUTE_PREFIX = f'{APIRoutes.API_ROUTE_PREFIX}{APIRoutes.API_AUTH_ROUTE_PREFIX}'

user_data = {"email": "ivan@gmail.com", "password": "12345678"}


def test_signup(client, monkeypatch):
    monkeypatch.setattr('src.services.mail.Mail.send_mail', MagicMock())

    response = client.post(
        f'{AUTH_ROUTE_PREFIX}/signup',
        json=user_data
    )

    assert response.status_code == status.HTTP_201_CREATED, response.text
    data = response.json()['data']
    assert data['email'] == user_data['email']
    assert 'id' in data
    assert "password" not in data


def test_signup_repeat(client, monkeypatch):
    monkeypatch.setattr('src.services.mail.Mail.send_mail', MagicMock())
    print('!!!!abc')
    response = client.post(
        f'{AUTH_ROUTE_PREFIX}/signup',
        json=user_data
    )

    print('!!!response.status_code!!!: ', response.status_code)

    # assert response.status_code == status.HTTP_409_CONFLICT

    # detail = response.json()['detail']
    # print('!!!!!!detail: ', detail)
    # assert detail == Messages.ACCOUNT_EXIST
