from datetime import datetime, timedelta, timezone
from typing import Dict, Tuple

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from car_api.core.database import get_session
from car_api.core.settings import Settings
from car_api.models.cars import Car
from car_api.models.users import User

pwd_context = PasswordHash.recommended()

settings = Settings()


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: Dict) -> Tuple[str, str]:
    to_encode = data.copy()
    to_encode_refresh = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.JWT_EXPIRATION_MINUTES
    )
    expire_refresh = datetime.now(timezone.utc) + timedelta(
        hours=settings.JWT_REFRESH_EXPIRATION_HOURS
    )
    to_encode.update({'exp': expire, 'type': 'access'})
    to_encode_refresh.update({'exp': expire_refresh, 'type': 'refresh'})

    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM
    )
    refresh_encoded_jwt = jwt.encode(
        to_encode_refresh, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM
    )

    return encoded_jwt, refresh_encoded_jwt


def verify_token(token: str) -> Dict:
    try:
        payload = jwt.decode(
            token,
            key=settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token inválido.',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token expirado. Por favor, faça login novamente.',
            headers={'WWW-Authenticate': 'Bearer'},
        )


oauth2_schema = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/')


async def valid_token(
    token: str = Depends(oauth2_schema),
    db: AsyncSession = Depends(get_session),
):
    payload = verify_token(token)

    if payload.get('type') != 'access':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Tipo de token inválido para esta rota.',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    user_id_str = payload.get('sub')

    if not user_id_str:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Credenciais inválidas.',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    try:
        user_id = int(user_id_str)

    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Credenciais inválidas.',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Credenciais inválidas.',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    return user


async def verify_user(user_id: int, user: User = Depends(valid_token)) -> None:
    if user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Sem permissão para realizar alterações neste usuário.',
        )


async def verify_car_owner(
    car_id: int,
    user: User = Depends(valid_token),
    db: AsyncSession = Depends(get_session),
):
    car_id_user_match = await db.scalar(
        select(exists().where((Car.owner_id == user.id) & (Car.id == car_id)))
    )

    if not car_id_user_match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Usuário não possui carro com este id.',
        )
