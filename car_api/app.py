from fastapi import Depends, FastAPI, HTTPException, Request, responses, status

from car_api.core.security import valid_token
from car_api.routers import auth, brands, cars, users

app = FastAPI(
    title='Car Management API',
    version='1.0.0',
    description='Sistema de gerenciamento de veículos com autenticação JWT',
)


@app.exception_handler(HTTPException)
async def error_expt(request: Request, exc: HTTPException):
    return responses.JSONResponse(
        status_code=exc.status_code,
        content={'error': exc.status_code, 'detail': exc.detail},
    )


app.include_router(
    router=users.router,
    prefix='/api/v1/users',
    tags=['users'],
)

app.include_router(
    router=brands.router,
    prefix='/api/v1/brands',
    tags=['brands'],
    dependencies=[Depends(valid_token)],
)

app.include_router(
    router=cars.router,
    prefix='/api/v1/cars',
    tags=['cars'],
    dependencies=[Depends(valid_token)],
)

app.include_router(
    router=auth.router,
    prefix='/api/v1/auth',
    tags=['token'],
)


@app.get('/health_check', status_code=status.HTTP_200_OK)
async def health_check():
    return {'status': 'ok'}
