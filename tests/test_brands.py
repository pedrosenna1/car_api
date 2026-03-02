from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_create_brand(client, token):
    response = client.post(
        '/api/v1/brands/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'Ford',
            'description': 'Ford Brand',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['name'] == 'ford'


@pytest.mark.asyncio
async def test_create_brand_already_exists(client, token, brand):
    response = client.post(
        '/api/v1/brands/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': brand.name,
            'description': 'Toyota Brand',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Marca já existe.'


@pytest.mark.asyncio
async def test_get_brand(client, token, brand):
    response = client.get(
        f'/api/v1/brands/{brand.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['name'] == brand.name


@pytest.mark.asyncio
async def test_list_brands(client, token, brand):
    response = client.get(
        '/api/v1/brands/',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert 'brands' in data
    assert len(data['brands']) > 0


@pytest.mark.asyncio
async def test_update_brand(client, token, brand):
    response = client.put(
        f'/api/v1/brands/{brand.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Updated Brand'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['name'] == 'Updated Brand'


@pytest.mark.asyncio
async def test_delete_brand(client, token, brand):
    response = client.delete(
        f'/api/v1/brands/{brand.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NO_CONTENT
