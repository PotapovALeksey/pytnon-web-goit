from unittest.mock import MagicMock

from starlette import status
import pytest

from src.config.constants import APIRoutes, Messages
import src.repository.user as user_repository

from tests.conftest import TestingSessionLocal

AUTH_ROUTE_PREFIX = f'{APIRoutes.API_ROUTE_PREFIX}{APIRoutes.API_AUTH_ROUTE_PREFIX}'

user_data = {"email": "ivan@gmail.com", "password": "12345678"}


def test_signup(client, monkeypatch):
    monkeypatch.setattr('src.services.mail.mail_service.send_mail', MagicMock())

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
    monkeypatch.setattr('src.services.mail.mail_service.send_mail', MagicMock())

    response = client.post(
        f'{AUTH_ROUTE_PREFIX}/signup',
        json=user_data
    )

    assert response.status_code == status.HTTP_409_CONFLICT, response.text
    message = response.json()['message']
    assert message == Messages.ACCOUNT_EXIST


def test_signin_not_confirmed(client, monkeypatch):
    response = client.post(
        f'{AUTH_ROUTE_PREFIX}/signin',
        json=user_data
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.text
    message = response.json()['message']
    assert message == Messages.EMAIL_NOT_CONFIRMED


@pytest.mark.asyncio
async def test_signin(client):
    async with TestingSessionLocal() as session:
        user = await user_repository.get_user_by_email(user_data['email'], session)
        await user_repository.confirm_user(user, session)

    response = client.post(
        f'{AUTH_ROUTE_PREFIX}/signin',
        json=user_data
    )

    assert response.status_code == status.HTTP_200_OK, response.text
    data = response.json()['data']
    assert 'access_token' in data
    assert 'refresh_token' in data

def test_signin_invalid_password(client):
    response = client.post(
        f'{AUTH_ROUTE_PREFIX}/signin',
        json={ 'email': user_data['email'], 'password': '12345679'}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.text
    message = response.json()['message']
    assert message == Messages.INVALID_CREDENTIALS


def test_signin_invalid_email(client):
    response = client.post(
        f'{AUTH_ROUTE_PREFIX}/signin',
        json={ 'email': 'asfdf@gmail.com', 'password': '12345679'}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.text
    message = response.json()['message']
    assert message == Messages.INVALID_CREDENTIALS