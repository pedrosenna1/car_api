from decimal import Decimal
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from car_api.core.database import get_session
from car_api.core.security import valid_token, verify_car_owner
from car_api.models.cars import Brand, Car, FuelType, TransmissionType
from car_api.models.users import User
from car_api.schemas.cars import (
    CarListPublicSchema,
    CarPublicSchema,
    CarSchema,
    CarUpdateSchema,
)

router = APIRouter()


@router.post(
    '/', status_code=status.HTTP_201_CREATED, response_model=CarPublicSchema
)
async def create_car(car: CarSchema, db: AsyncSession = Depends(get_session)):
    new_car = Car(
        model=car.model,
        factory_year=car.factory_year,
        model_year=car.model_year,
        color=car.color,
        plate=car.plate,
        fuel_type=car.fuel_type,
        transmission=car.transmission,
        price=car.price,
        description=car.description,
        is_available=car.is_available,
        brand_id=car.brand_id,
        owner_id=car.owner_id,
    )

    owner_exists = await db.scalar(
        select(exists().where(User.id == car.owner_id))
    )

    if not owner_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Proprietário não existe.',
        )

    brand_not_active = await db.scalar(
        select(exists().where(Brand.id == car.brand_id, Brand.is_active))
    )

    if not brand_not_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Marca não existe ou não está ativada.',
        )

    plate_exists = await db.scalar(
        select(exists().where(Car.plate == car.plate))
    )

    if plate_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Placa já cadastrada.',
        )

    db.add(new_car)
    await db.commit()
    await db.refresh(new_car)

    result = await db.execute(
        select(Car)
        .options(selectinload(Car.brand), selectinload(Car.owner))
        .where(Car.id == new_car.id)
    )

    car_with_relations = result.scalar_one()

    return car_with_relations


@router.get(
    '/{car_id}',
    status_code=status.HTTP_200_OK,
    response_model=CarPublicSchema,
)
async def get_car(
    car_id: int,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(valid_token),
):
    result = await db.execute(
        select(Car)
        .options(selectinload(Car.brand), selectinload(Car.owner))
        .where(Car.id == car_id)
    )
    car_with_relations = result.scalar_one_or_none()

    if not car_with_relations or (
        car_with_relations.owner_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Carro não encontrado.',
        )

    return car_with_relations


@router.get(
    '/', status_code=status.HTTP_200_OK, response_model=CarListPublicSchema
)
async def get_all_cars(
    search: Optional[str] = Query(
        default=None, description='Buscar por modelo, cor ou placa.'
    ),
    fuel: Optional[List[FuelType]] = Query(
        default=None, description='Filtrar por tipo de combustivel.'
    ),
    transmission: Optional[List[TransmissionType]] = Query(
        default=None, description='Filtrar por tipo de transmissão.'
    ),
    is_available: Optional[bool] = Query(
        default=None, description='Filtrar por disponibilidade'
    ),
    limit: int = Query(
        default=100, ge=1, le=1000, description='Limite de registros.'
    ),
    offset: int = Query(
        default=0, ge=0, description='Número de registros para pular.'
    ),
    brand_id: Optional[int] = Query(
        default=None, description='Filtrar por marca.'
    ),
    owner_id: Optional[int] = Query(
        default=None, description='Filtrar por proprietário.'
    ),
    min_price: Optional[Decimal] = Query(
        default=None,
        max_digits=10,
        decimal_places=2,
        description='Filtrar por preço minimo.',
    ),
    max_price: Optional[Decimal] = Query(
        default=None,
        max_digits=10,
        decimal_places=2,
        description='Filtrar por preço máximo.',
    ),
    current_user: User = Depends(valid_token),
    db: AsyncSession = Depends(get_session),
):

    query = select(Car).options(
        selectinload(Car.brand), selectinload(Car.owner)
    )
    query = query.where(Car.owner_id == current_user.id)

    if search:
        search_filter = f'%{search}%'
        query = query.where(
            (Car.model.ilike(search_filter))
            | (Car.color.ilike(search_filter))
            | (Car.plate.ilike(search_filter))
        )

    if brand_id is not None:
        query = query.where(Car.brand_id == brand_id)

    if owner_id is not None:
        query = query.where(Car.owner_id == owner_id)

    if fuel is not None:
        query = query.where(Car.fuel_type.in_(fuel))

    if transmission is not None:
        query = query.where(Car.transmission.in_(transmission))

    if is_available is not None:
        query = query.where(Car.is_available == is_available)

    if max_price is not None:
        query = query.where(Car.price <= max_price)

    if min_price is not None:
        query = query.where(Car.price >= min_price)

    query = query.limit(limit).offset(offset)

    result = await db.execute(query)
    results = result.scalars().all()
    return {'cars': results, 'offset': offset, 'limit': limit}


@router.put(
    '/{car_id}',
    status_code=status.HTTP_200_OK,
    response_model=CarPublicSchema,
    dependencies=[Depends(verify_car_owner)],
)
async def update_car(
    car_id: int,
    car_update: CarUpdateSchema,
    db: AsyncSession = Depends(get_session),
):
    car = await db.get(Car, car_id)
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Carro não encontrado.',
        )

    update_data = car_update.model_dump(exclude_unset=True)

    if 'plate' in update_data and update_data['plate'] != car.plate:
        car_plate_exists = await db.scalar(
            select(
                exists().where(
                    (Car.plate == update_data['plate']) & (Car.id != car_id)
                )
            )
        )

        if car_plate_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Placa já existe.',
            )

    if 'brand_id' in update_data:
        brand_exists = await db.scalar(
            select(exists().where(Brand.id == update_data['brand_id']))
        )

        if not brand_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Marca não encontrada.',
            )

    if 'owner_id' in update_data:
        owner_exists = await db.scalar(
            select(exists().where(User.id == update_data['owner_id']))
        )

        if not owner_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Proprietário não encontrada.',
            )

    for key, value in update_data.items():
        setattr(car, key, value)

    await db.commit()
    await db.refresh(car)

    result = await db.execute(
        select(Car)
        .where(Car.id == car_id)
        .options(selectinload(Car.brand), selectinload(Car.owner))
    )
    car_with_relations = result.scalar_one()

    return car_with_relations


@router.delete(
    '/{car_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(verify_car_owner)],
)
async def delete_car(car_id: int, db: AsyncSession = Depends(get_session)):
    car = await db.get(Car, car_id)
    if not car:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail='Carro não encontrado.'
        )

    await db.delete(car)
    await db.commit()
