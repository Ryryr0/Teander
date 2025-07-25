from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from typing import Annotated
import jwt

from fastapi import APIRouter, Form, Body, Path
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from fastapi.responses import HTMLResponse

from config import settings
from database.queries import Queries
from logger import Logger
from schemas import Token, UserDTO, UserPostDTO, TokenData
from dependencies import get_user_post_form, get_token_data


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "User not found"}},
)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class HashedPWD:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)


async def authenticate_user(username: str, password: str):
    user = await Queries.get_user(username)
    if not user or user.disabled:
        return False
    if not HashedPWD.verify_password(password, user.hashed_password):
        return False
    Logger.info(f"User <username: {user.username}> was authenticated")
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.PRIVATE_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    Logger.info(f"Token was issued for user <id: {user.id}, username: {user.username}>")
    return Token(access_token=access_token, token_type="bearer")


@router.post("/reg")
async def registrate_user(
        form_data: Annotated[UserPostDTO, Depends(get_user_post_form)],
        password: Annotated[str, Form()],
):
    try:
        user = UserDTO(
            **form_data.model_dump(),
            hashed_password=HashedPWD.get_password_hash(password)
        )
        user_id = await Queries.post_user(user)
    except ValueError as ex:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=ex.args,
        )
    Logger.info(f"User <username: {user.username}> was created")
    return HTMLResponse(status_code=status.HTTP_201_CREATED)


@router.put("/update-user")
async def update_user(
        token_data: Annotated[TokenData, Depends(get_token_data)],
        new_user_data: Annotated[UserPostDTO, Depends(get_user_post_form)]
):
    try:
        await Queries.update_user(token_data.id, new_user_data)
    except ValueError as ex:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=ex.args,
        )
    Logger.info(f"User <id: {token_data.id}> was updated")


@router.delete("/delete")
async def delete_user(token_data: Annotated[TokenData, Depends(get_token_data)]):
    try:
        await Queries.delete_user(token_data.id)
    except ValueError as ex:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=ex.args[0],
        )
    Logger.info(f"User <id: {token_data.id}> was deleted")
