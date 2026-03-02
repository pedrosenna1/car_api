from http import HTTPStatus

import pytest

from car_api.models.cars import Car


@pytest.mark.asyncio
async def test_create_car(client, token, user, brand):
    response = client.post(
        '/api/v1/cars/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'model': 'Corolla',
            'factory_year': 2022,
            'model_year': 2023,
            'color': 'Silver',
            'plate': 'ABC1D23',
            'fuel_type': 'flex',
            'transmission': 'automatic',
            'price': 120000.00,
            'brand_id': brand.id,
            'owner_id': user.id,
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['model'] == 'Corolla'


@pytest.mark.asyncio
async def test_create_car_invalid_brand(client, token, user):
    response = client.post(
        '/api/v1/cars/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'model': 'Corolla',
            'factory_year': 2022,
            'model_year': 2023,
            'color': 'Silver',
            'plate': 'ABC1D24',
            'fuel_type': 'flex',
            'transmission': 'automatic',
            'price': 120000.00,
            'brand_id': 999,
            'owner_id': user.id,
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_create_car_invalid_owner(client, token, brand):
    response = client.post(
        '/api/v1/cars/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'model': 'Corolla',
            'factory_year': 2022,
            'model_year': 2023,
            'color': 'Silver',
            'plate': 'ABC1D25',
            'fuel_type': 'flex',
            'transmission': 'automatic',
            'price': 120000.00,
            'brand_id': brand.id,
            'owner_id': 999,  # Non-existent owner_id
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Proprietário não existe.'


@pytest.mark.asyncio
async def test_create_car_duplicate_plate(client, token, user, brand):
    response = client.post(
        '/api/v1/cars/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'model': 'Corolla',
            'factory_year': 2022,
            'model_year': 2023,
            'color': 'Blue',
            'plate': 'XYZ1234',
            'fuel_type': 'gasoline',
            'transmission': 'manual',
            'price': 90000.00,
            'brand_id': brand.id,
            'owner_id': user.id,
        },
    )
    assert response.status_code == HTTPStatus.CREATED

    response = client.post(
        '/api/v1/cars/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'model': 'Civic',
            'factory_year': 2021,
            'model_year': 2022,
            'color': 'Red',
            'plate': 'XYZ1234',  # Duplicate plate
            'fuel_type': 'flex',
            'transmission': 'automatic',
            'price': 110000.00,
            'brand_id': brand.id,
            'owner_id': user.id,
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Placa já cadastrada.'


@pytest.mark.asyncio
async def test_list_cars(session, client, token, user, brand):
    session.add(
        Car(
            model='Corolla',
            factory_year=2022,
            model_year=2023,
            color='Silver',
            plate='ABC1D23',
            fuel_type='flex',
            transmission='automatic',
            price=120000.00,
            brand_id=brand.id,
            owner_id=user.id,
        )
    )
    await session.commit()

    response = client.get(
        '/api/v1/cars/',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert 'cars' in data
    assert len(data['cars']) == 1


@pytest.mark.asyncio
async def test_get_car(session, client, token, user, brand):
    car = Car(
        model='Corolla',
        factory_year=2022,
        model_year=2023,
        color='Silver',
        plate='ABC1D23',
        fuel_type='flex',
        transmission='automatic',
        price=120000.00,
        brand_id=brand.id,
        owner_id=user.id,
    )
    session.add(car)
    await session.commit()
    await session.refresh(car)

    response = client.get(
        f'/api/v1/cars/{car.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['model'] == 'Corolla'


@pytest.mark.asyncio
async def test_get_car_not_found(client, token):
    response = client.get(
        '/api/v1/cars/999',  # Non-existent car_id
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == 'Carro não encontrado.'


@pytest.mark.asyncio
async def test_update_car(session, client, token, user, brand):
    car = Car(
        model='Corolla',
        factory_year=2022,
        model_year=2023,
        color='Silver',
        plate='ABC1D23',
        fuel_type='flex',
        transmission='automatic',
        price=120000.00,
        brand_id=brand.id,
        owner_id=user.id,
    )
    session.add(car)
    await session.commit()
    await session.refresh(car)

    response = client.put(
        f'/api/v1/cars/{car.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'model': 'Corolla Updated'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['model'] == 'Corolla Updated'


@pytest.mark.asyncio
async def test_delete_car(session, client, token, user, brand):
    car = Car(
        model='Corolla',
        factory_year=2022,
        model_year=2023,
        color='Silver',
        plate='ABC1D23',
        fuel_type='flex',
        transmission='automatic',
        price=120000.00,
        brand_id=brand.id,
        owner_id=user.id,
    )
    session.add(car)
    await session.commit()
    await session.refresh(car)

    response = client.delete(
        f'/api/v1/cars/{car.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NO_CONTENT


async def create_test_cars(session, user, brand):
    cars_to_create = [
        Car(
            model='Model S',
            factory_year=2022,
            model_year=2023,
            color='Red',
            plate='TESL4S',
            fuel_type='eletric',
            transmission='automatic',
            price=450000.00,
            brand_id=brand.id,
            owner_id=user.id,
        ),
        Car(
            model='Mustang',
            factory_year=2022,
            model_year=2023,
            color='Blue',
            plate='MUST4NG',
            fuel_type='gasoline',
            transmission='manual',
            price=350000.00,
            brand_id=brand.id,
            owner_id=user.id,
        ),
    ]
    session.add_all(cars_to_create)
    await session.commit()


@pytest.mark.asyncio
async def test_list_cars_search_by_model(session, client, token, user, brand):
    await create_test_cars(session, user, brand)
    response = client.get(
        '/api/v1/cars/?search=Model S',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['cars']) == 1
    assert response.json()['cars'][0]['model'] == 'Model S'


@pytest.mark.asyncio
async def test_list_cars_filter_by_fuel(session, client, token, user, brand):
    await create_test_cars(session, user, brand)
    response = client.get(
        '/api/v1/cars/?fuel=eletric',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['cars']) == 1
    assert response.json()['cars'][0]['fuel_type'] == 'eletric'


@pytest.mark.asyncio
async def test_list_cars_filter_by_transmission(
    session, client, token, user, brand
):
    await create_test_cars(session, user, brand)
    response = client.get(
        '/api/v1/cars/?transmission=manual',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['cars']) == 1
    assert response.json()['cars'][0]['transmission'] == 'manual'


@pytest.mark.asyncio
async def test_list_cars_filter_by_price(session, client, token, user, brand):
    await create_test_cars(session, user, brand)
    response = client.get(
        '/api/v1/cars/?min_price=400000',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['cars']) == 1
    assert response.json()['cars'][0]['price'] == '450000.00'

    response = client.get(
        '/api/v1/cars/?max_price=400000',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['cars']) == 1
    assert response.json()['cars'][0]['price'] == '350000.00'
