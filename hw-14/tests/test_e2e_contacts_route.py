from unittest.mock import MagicMock, patch, AsyncMock

from starlette import status
import pytest

from src.config.constants import APIRoutes

CONTACTS_ROUTE_PREFIX = f'{APIRoutes.API_ROUTE_PREFIX}{APIRoutes.API_CONTACTS_ROUTE_PREFIX}'

contact_data = {
    "name": "Ivan",
    "surname": "Ivanov",
    "birthday": "2000-01-01",
    "email": "n7t8c@example.com",
    "phone": "123456789"
}

contact_id = 1

def test_create_contact(client, token, monkeypatch):
    mocked_redis = MagicMock
    mocked_redis.get = AsyncMock(return_value=None)

    with patch('src.database.cache.get_cache', mocked_redis):
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        headers = {'Authorization': f'Bearer {token}'}
        response = client.post(
            CONTACTS_ROUTE_PREFIX,
            headers=headers,
            json=contact_data
        )

        assert response.status_code == status.HTTP_201_CREATED, response.text
        data = response.json()['data']
        assert 'id' in data
        assert data['name'] == contact_data['name']
        assert data['surname'] == contact_data['surname']
        assert data['email'] == contact_data['email']
        assert data['phone'] == contact_data['phone']


def test_get_contact(client, token, monkeypatch):
    mocked_redis = MagicMock
    mocked_redis.get = AsyncMock(return_value=None)

    with patch('src.database.cache.get_cache', mocked_redis):
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        headers = {'Authorization': f'Bearer {token}'}
        response = client.get(
            f'{CONTACTS_ROUTE_PREFIX}/{contact_id}',
            headers=headers,
        )

        assert response.status_code == status.HTTP_200_OK, response.text
        data = response.json()['data']
        assert data['name'] == contact_data['name']
        assert data['id'] == contact_id


def test_get_contacts(client, token, monkeypatch):
    mocked_redis = MagicMock
    mocked_redis.get = AsyncMock(return_value=None)

    with patch('src.database.cache.get_cache', mocked_redis):
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        headers = {'Authorization': f'Bearer {token}'}
        response = client.get(
            CONTACTS_ROUTE_PREFIX,
            headers=headers,
        )

        assert response.status_code == status.HTTP_200_OK, response.text
        contacts = response.json()['data']
        assert contacts[0]['id'] == contact_id


def test_update_contact(client, token, monkeypatch):
    mocked_redis = MagicMock
    mocked_redis.get = AsyncMock(return_value=None)

    with patch('src.database.cache.get_cache', mocked_redis):
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        headers = {'Authorization': f'Bearer {token}'}

        new_name = 'Petr'

        response = client.patch(
            f'{CONTACTS_ROUTE_PREFIX}/{contact_id}',
            headers=headers,
            json={
                **contact_data,
                'name': new_name
            }
        )

        assert response.status_code == status.HTTP_200_OK, response.text
        data = response.json()['data']
        assert data['name'] == new_name


def test_update_contact_not_exist(client, token, monkeypatch):
    mocked_redis = MagicMock
    mocked_redis.get = AsyncMock(return_value=None)

    with patch('src.database.cache.get_cache', mocked_redis):
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        headers = {'Authorization': f'Bearer {token}'}

        new_name = 'Petr'
        not_exist_contact_id = 2
        response = client.patch(
            f'{CONTACTS_ROUTE_PREFIX}/{not_exist_contact_id}',
            headers=headers,
            json={
                **contact_data,
                'name': new_name
            }
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND, response.text


def test_delete_contact(client, token, monkeypatch):
    mocked_redis = MagicMock
    mocked_redis.get = AsyncMock(return_value=None)

    with patch('src.database.cache.get_cache', mocked_redis):
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        headers = {'Authorization': f'Bearer {token}'}
        response = client.delete(
            f'{CONTACTS_ROUTE_PREFIX}/{contact_id}',
            headers=headers,
        )

        assert response.status_code == status.HTTP_200_OK, response.text


def test_delete_not_exist_contact(client, token, monkeypatch):
    mocked_redis = MagicMock
    mocked_redis.get = AsyncMock(return_value=None)

    with patch('src.database.cache.get_cache', mocked_redis):
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        headers = {'Authorization': f'Bearer {token}'}
        response = client.delete(
            f'{CONTACTS_ROUTE_PREFIX}/{contact_id}',
            headers=headers,
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND, response.text