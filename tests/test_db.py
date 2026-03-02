import pytest
from sqlalchemy import select

from car_api.models.cars import Brand, Car, FuelType, TransmissionType
from car_api.models.users import User


@pytest.mark.asyncio
async def test_db_connection(session):
    assert session.is_active


@pytest.mark.asyncio
async def test_create_user_in_db(session):
    new_user = User(
        username='pedro', password='secret', email='teste@test.com'
    )
    session.add(new_user)
    await session.commit()

    user = await session.scalar(
        select(User).where(User.email == 'teste@test.com')
    )
    assert user is not None
    assert user.username == 'pedro'


@pytest.mark.asyncio
async def test_create_brand_and_car_in_db(session):
    new_brand = Brand(name='toyota', is_active=True)
    session.add(new_brand)
    await session.commit()
    await session.refresh(new_brand)

    new_user = User(
        username='owner', password='password', email='owner@test.com'
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    new_car = Car(
        model='Corolla',
        factory_year=2022,
        model_year=2023,
        color='Silver',
        plate='ABC1D23',
        fuel_type=FuelType.FLEX,
        transmission=TransmissionType.AUTOMATIC,
        price=120000.00,
        brand_id=new_brand.id,
        owner_id=new_user.id
    )
    session.add(new_car)
    await session.commit()

    car = await session.scalar(select(Car).where(Car.plate == 'ABC1D23'))
    assert car is not None
    assert car.model == 'Corolla'
    assert car.brand_id == new_brand.id
