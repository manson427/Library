from fastapi import (
    APIRouter, Depends, HTTPException, Response, status, Request, Body, Path,
    Cookie
)

from app.api.schemas.all import  UserRegister, UserDBPublic, UserAdd

from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from app.api.utils.security import get_password_hash, create_token, verify_password, require_user
from app.db.database import get_rep, Repository

from app.config import settings
from datetime import timedelta
from app.api.schemas.auth import Tokens

from app.log.logger import logger


auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@auth_router.post("/register/", response_model=UserDBPublic)
async def register(user_register: UserRegister, rep: Repository = Depends(get_rep)):
    if await rep.user.get_by_name(user_register.name):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail='Account already exist')

    if user_register.password != user_register.password_confirm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Passwords do not match')

    user_add = UserAdd(**(
            user_register.__dict__ |
            {'hashed_password': get_password_hash(user_register.password)}))
    res = await rep.user.create(user_add.model_dump())
    user = res.to_schema_public()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error creating user')
    logger.debug(f"User {user.id} created")
    return user


# В случае успеха возвращает cookies с access и refresh токенами
@auth_router.post("/login/", status_code=status.HTTP_200_OK, response_model=Tokens)
async def login(
        response: Response,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        rep: Repository = Depends(get_rep),
):
    res = await rep.user.get_by_name(form_data.username)
    user = res.to_schema()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
    # if not user.verified:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED, detail='Please verify your email address')

    access_token: str = create_token(
        subject={"sub": str(user.id)}, expires_time=timedelta(minutes=settings.ACCESS_MINUTES))
    refresh_token: str = create_token(
        subject={"sub": str(user.id)}, expires_time=timedelta(days=settings.REFRESH_DAYS))
    tokens = Tokens(access_token=access_token, refresh_token=refresh_token)
    response.set_cookie("access_token", tokens.access_token, httponly=True)
    response.set_cookie("refresh_token", tokens.refresh_token, httponly=True)
    logger.debug(f"User {user.id} logged in")
    return tokens.model_dump()


@auth_router.post('/logout/', status_code=status.HTTP_200_OK)
async def logout(request: Request, response: Response, user_id = Depends(require_user)):
    response.delete_cookie('access_token', path='/', domain=None)
    response.delete_cookie('refresh_token', path='/', domain=None)
    message = f"User {user_id} logged out"
    logger.debug(message)
    return {'message': message}