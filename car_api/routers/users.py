from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import exists, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from car_api.core.database import get_session
from car_api.core.security import (
    get_password_hash,
    valid_token,
    verify_user,
)
from car_api.models.users import User
from car_api.schemas.users import (
    UserListPublicSchema,
    UserPublicSchema,
    UserSchema,
    UserUpdateSchema,
)

router = APIRouter()


@router.get(
    path='/',
    status_code=status.HTTP_200_OK,
    response_model=UserListPublicSchema,
    dependencies=[Depends(valid_token)],
    summary='Listar usuários',
)
async def list_users(
    offset: int = Query(0, ge=0, description='Número de regitros para pular'),
    limit: int = Query(100, ge=1, le=100, description='Limite de registros'),
    search: Optional[str] = Query(
        None, description='Buscar por username ou email'
    ),
    db: AsyncSession = Depends(get_session),
):

    query = select(User)
    query_total_results = select(func.count(User.id))
    if search:
        search_filter = f'%{search}%'
        query = query.where(
            User.username.ilike(search_filter)
            | User.email.ilike(search_filter)
        )
        query_total_results = query_total_results.where(
            User.username.ilike(search_filter)
            | User.email.ilike(search_filter)
        )

    query = query.offset(offset).limit(limit)
    total_results = await db.execute(query_total_results)
    total_results = total_results.scalar()
    result = await db.execute(query)
    users = result.scalars().all()

    return {
        'users': users,
        'offset': offset,
        'limit': limit,
        'total_results': total_results,
    }


@router.get(
    '/{user_id}',
    status_code=status.HTTP_200_OK,
    response_model=UserPublicSchema,
    dependencies=[Depends(valid_token)],
    summary='Buscar usuário por id',
)
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Usuário não encontrado',
        )

    return user


@router.post(
    path='/add_user',
    status_code=status.HTTP_201_CREATED,
    response_model=UserPublicSchema,
    summary='Criar novo usuário',
)
async def create_user(
    form: UserSchema, db: AsyncSession = Depends(get_session)
):

    username_exists = await db.scalar(
        select(exists().where(User.username == form.username))
    )
    email_exists = await db.scalar(
        select(exists().where(User.email == form.email))
    )

    if username_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Username já está sendo usado',
        )

    if email_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email já está sendo usado',
        )

    db_user = User(
        username=form.username,
        email=form.email,
        password=get_password_hash(form.password),
    )

    try:
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)

        return db_user

    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f'Não foi possível adicionar o usuário: {str(e)}',
        )


@router.put(
    path='/{user_id}',
    status_code=status.HTTP_200_OK,
    response_model=UserPublicSchema,
    dependencies=[Depends(verify_user), Depends(valid_token)],
    summary='Atualizar usuáio',
)
async def update_user(
    user_id: int,
    user_update: UserUpdateSchema,
    db: AsyncSession = Depends(get_session),
):

    user = await db.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Usuário não encontrado',
        )

    update_data = user_update.model_dump(exclude_unset=True)

    if 'username' in update_data and update_data['username'] != user.username:
        username_exists = await db.scalar(
            select(
                exists().where(
                    (User.username == update_data['username'])
                    & (User.id != user_id)
                )
            )
        )

        if username_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Username já está sendo usado',
            )

    if 'email' in update_data and update_data['email'] != user.email:
        email_exists = await db.scalar(
            select(
                exists().where(
                    (User.email == update_data['email']) & (User.id != user_id)
                )
            )
        )

        if email_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Email já está sendo usado',
            )

    if 'password' in update_data:
        update_data['password'] = get_password_hash(update_data['password'])

    for key, value in update_data.items():
        setattr(user, key, value)

    try:
        await db.commit()
        await db.refresh(user)
        return user
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Erro ao atualizar usuário',
        )


@router.delete(
    '/{user_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(verify_user), Depends(valid_token)],
    summary='Deletar usuário',
)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_session)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Usuário não encontrado',
        )

    await db.delete(user)
    await db.commit()
