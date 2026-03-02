from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_create_user(client):
    response = client.post(
        '/api/v1/users/add_user',
        json={
            'username': 'newuser',
            'email': 'newuser@test.com',
            'password': 'password123',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert data['username'] == 'newuser'
    assert data['email'] == 'newuser@test.com'
    assert 'id' in data


@pytest.mark.asyncio
async def test_create_user_already_exists(client, user):
    response = client.post(
        '/api/v1/users/add_user',
        json={
            'username': user.username,
            'email': 'different@test.com',
            'password': 'password123',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Username já está sendo usado'


@pytest.mark.asyncio
async def test_list_users(client, token):
    response = client.get(
        '/api/v1/users/',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert 'users' in data
    assert len(data['users']) > 0


@pytest.mark.asyncio
async def test_get_user(client, token, user):
    response = client.get(
        f'/api/v1/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['username'] == user.username


@pytest.mark.asyncio
async def test_update_user(client, token, user):
    response = client.put(
        f'/api/v1/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'username': 'updateduser'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['username'] == 'updateduser'


@pytest.mark.asyncio
async def test_delete_user(client, token, user):
    response = client.delete(
        f'/api/v1/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NO_CONTENT
