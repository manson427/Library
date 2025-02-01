from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2AuthorizationCodeBearer
from jose import jwt, JWTError
from app.config import settings
from typing import Any
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status, Response, Request
from app.api.schemas.auth import Tokens
from app.api.exceptions.auth import AuthenticationError
from app.log.logger import logger
from app.db.database import get_rep, Repository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password, hashed_password) -> bool:
    if not pwd_context.verify(password + settings.SALT, hashed_password):
        raise AuthenticationError
    return True


def get_password_hash(password) -> Any:
    return pwd_context.hash(password + settings.SALT)


def create_token(subject: dict, expires_time: timedelta) -> str:
    to_encode = subject.copy()
    expire = datetime.now() + expires_time
    encoded_jwt = jwt.encode(
        to_encode | {"exp": expire},
        settings.JWT_SECRET_KEY.get_secret_value(),
        algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

async def require_user(
        request: Request,
        response: Response,
        rep: Repository = Depends(get_rep),) -> int:
    access_token = request.cookies.get("access_token")
    try:
        payload = jwt.decode(
            access_token,
            settings.JWT_SECRET_KEY.get_secret_value(),
            algorithms=[settings.JWT_ALGORITHM])
    except AttributeError or JWTError: #AccessTokenExpired:
        tokens = await refresh(request, response)
        payload = jwt.decode(
            tokens.access_token,
            settings.JWT_SECRET_KEY.get_secret_value(),
            algorithms=[settings.JWT_ALGORITHM])

    try:
        user_id = int(payload.get("sub"))
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Fake token')

    user = await rep.user.get_one(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Fake token')

    # if not user.verified:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN, detail='Please verify your account')
    return int(payload.get("sub"))


async def refresh(request: Request, response: Response) -> Tokens:
    try:
        refresh_token = request.cookies.get("refresh_token")
        payload = jwt.decode(refresh_token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except AttributeError or JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
    access_token: str = create_token(
        subject={"sub": payload.get("sub")}, expires_time=timedelta(minutes=settings.ACCESS_MINUTES))
    refresh_token: str = create_token(
        subject={"sub": payload.get("sub")}, expires_time=timedelta(days=settings.REFRESH_DAYS))
    tokens = Tokens(access_token=access_token, refresh_token=refresh_token)
    response.set_cookie("access_token", tokens.access_token, httponly=True)
    response.set_cookie("refresh_token", tokens.refresh_token, httponly=True)
    logger.debug(f"Tokens refreshed for user {payload.get('sub')}")
    return tokens

