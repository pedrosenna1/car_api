from datetime import datetime, timedelta, timezone

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from car_api.core.database import get_session
from car_api.core.security import create_access_token, verify_password
from car_api.core.settings import Settings
from car_api.models.users import User
from car_api.schemas.auth import RefreshToken, Token

router = APIRouter()

settings = Settings()


@router.post(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=Token,
    description="Esta rota recebe o e-mail no campo 'username'",
    summary="Obter token padrão OAuth2 recebendo e-mail no campo 'username'",
)
async def token(
    form: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session),
):
    if len(form.username) < 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Username muito curto',
        )
    if len(form.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Senha muito curta'
        )

    user = await db.execute(select(User).where(User.email == form.username))
    user = user.scalar_one_or_none()

    if not user or not verify_password(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Usuário ou senha incorretos.',
        )

    payload = {
        'sub': str(user.id),
    }

    token, token_refesh = create_access_token(payload)

    return {
        'access_token': token,
        'refresh_token': token_refesh,
        'token_type': 'bearer',
    }


@router.post('/refresh', status_code=status.HTTP_201_CREATED)
async def refresh_token(token: RefreshToken):
    try:
        refresh_token = jwt.decode(
            token.refresh_token,
            key=settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )

        if refresh_token['type'] != 'refresh':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Refresh token inválido.',
            )

        new_access_token = jwt.encode(
            {
                'sub': refresh_token['sub'],
                'exp': datetime.now(tz=timezone.utc)
                + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES),
                'type': 'access',
            },
            key=settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )
        return {
            'access_token': new_access_token,
            'refresh_token': token.refresh_token,
            'token_type': 'bearer',
        }
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Token inválido.'
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token expirado. Por favor, faça login novamente.',
        )
