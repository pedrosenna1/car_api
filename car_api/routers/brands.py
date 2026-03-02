from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from car_api.core.database import get_session
from car_api.models.cars import Brand, Car
from car_api.schemas.brands import (
    BrandListPublicSchema,
    BrandPublicSchema,
    BrandSchema,
    BrandUpdateSchema,
)

router = APIRouter()


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=BrandPublicSchema,
    summary='Criar nova marca.',
)
async def create_brand(
    brand: BrandSchema, db: AsyncSession = Depends(get_session)
):
    result = await db.scalar(
        select((exists().where(Brand.name == brand.name.lower())))
    )
    if result:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail='Marca já existe.'
        )

    db_brand = Brand(
        name=brand.name.lower(),
        description=brand.description,
        is_active=brand.is_active,
    )
    db.add(db_brand)
    await db.commit()
    await db.refresh(db_brand)

    return db_brand


@router.get(
    '/{brand_id}',
    status_code=status.HTTP_200_OK,
    response_model=BrandPublicSchema,
    summary='Buscar marca por id.',
)
async def get_brand(brand_id: int, db: AsyncSession = Depends(get_session)):
    brand = await db.get(Brand, brand_id)

    if not brand:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail='Marca não encontrada.'
        )

    return brand


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=BrandListPublicSchema,
    summary='Listar todas as marcas',
)
async def get_all_brands(
    limit: int | None = Query(default=1, ge=1, le=1000),
    offset: int | None = Query(default=0, ge=0),
    search: Optional[List[str]] = Query(
        default=None, description='Buscar marcas por nome.'
    ),
    is_active: Optional[bool] = Query(default=None),
    db: AsyncSession = Depends(get_session),
):

    query = select(Brand)

    if search:
        query = query.filter(
            Brand.name.in_([marca.lower() for marca in search])
        )

    if is_active is not None:
        query = query.where(Brand.is_active == is_active)

    if limit:
        query = query.limit(limit=limit)
    if offset:
        query = query.offset(offset=offset)

    result = await db.execute(query)
    brands = result.scalars().all()

    return {'brands': brands, 'offset': offset, 'limit': limit}


@router.put(
    '/{brand_id}',
    status_code=status.HTTP_200_OK,
    response_model=BrandPublicSchema,
    summary='Atualizar cadastro de marca',
)
async def update_brand(
    brand_id: int,
    brand_update: BrandUpdateSchema,
    db: AsyncSession = Depends(get_session),
):
    brand = await db.get(Brand, brand_id)
    if not brand:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail='Marca não encontrada.'
        )

    update_data = brand_update.model_dump(exclude_unset=True)

    if 'name' in update_data and update_data['name'] != brand.name:
        name_exists = await db.scalar(
            select(
                exists().where(
                    (Brand.name == update_data['name'])
                    & (Brand.id != brand_id)
                )
            )
        )
        if name_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Nome da marca já está em uso.',
            )

    for key, value in update_data.items():
        setattr(brand, key, value)

    await db.commit()
    await db.refresh(brand)

    return brand


@router.delete(
    '/{brand_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Deletar marca.',
)
async def delete_brand(brand_id: int, db: AsyncSession = Depends(get_session)):
    brand = await db.get(Brand, brand_id)
    if not brand:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Marca não encontrada.',
        )

    brand_exists_incar = await db.scalar(
        select(exists().where(Car.brand_id == brand_id))
    )

    if brand_exists_incar:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Não é possivel deletar marca que possui carros associados',
        )

    await db.delete(brand)
    await db.commit()
