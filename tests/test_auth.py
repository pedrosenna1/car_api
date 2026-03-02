from http import HTTPStatus

import pytest

from car_api.core.security import create_access_token


@pytest.mark.asyncio
async def test_token_success(client, user, user_data):
    login_data = {
        'username': user_data['email'],
        'password': user_data['password'],
    }

    resp = client.post('/api/v1/auth/', data=login_data)

    assert resp.status_code == HTTPStatus.OK
    data = resp.json()

    assert 'access_token' in data
    assert 'refresh_token' in data
    assert data['token_type'] == 'bearer'
    assert isinstance(data['access_token'], str)
    assert len(data['access_token']) > 0


@pytest.mark.asyncio
async def test_token_usernamelow(client, user, user_data):
    login_data = {
        'username': 'pe',
        'password': user_data['password'],
    }

    resp = client.post('/api/v1/auth/', data=login_data)

    assert resp.status_code == HTTPStatus.BAD_REQUEST
    data = resp.json()
    assert data['detail'] == 'Username muito curto'


@pytest.mark.asyncio
async def test_token_passlow(client, user, user_data):
    login_data = {
        'username': user_data['email'],
        'password': '12333',
    }

    resp = client.post('/api/v1/auth/', data=login_data)

    assert resp.status_code == HTTPStatus.BAD_REQUEST
    data = resp.json()
    assert data['detail'] == 'Senha muito curta'


@pytest.mark.asyncio
async def test_token_incorrect(client, user, user_data):
    login_data = {
        'username': user_data['email'],
        'password': '12333333',
    }

    resp = client.post('/api/v1/auth/', data=login_data)

    assert resp.status_code == HTTPStatus.BAD_REQUEST
    data = resp.json()
    assert data['detail'] == 'Usuário ou senha incorretos.'


@pytest.mark.asyncio
async def test_refresh_token(client, user):
    payload = {'sub': str(user.id)}
    token, refresh_token = create_access_token(payload)
    payload = {'refresh_token': refresh_token}
    resp = client.post('/api/v1/auth/refresh', json=payload)
    assert resp.status_code == HTTPStatus.CREATED


@pytest.mark.asyncio
async def test_refresh_token_invalid_type(client, user):
    payload = {'sub': str(user.id)}
    token, refresh_token = create_access_token(payload)
    payload = {'refresh_token': token}
    resp = client.post('/api/v1/auth/refresh', json=payload)
    assert resp.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.asyncio
async def test_refresh_token_invalid(client, user):
    payload = {'sub': str(user.id)}
    token, refresh_token = create_access_token(payload)
    payload = {'refresh_token': token + '123'}
    resp = client.post('/api/v1/auth/refresh', json=payload)
    assert resp.status_code == HTTPStatus.UNAUTHORIZED
