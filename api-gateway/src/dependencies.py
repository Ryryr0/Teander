from typing import Annotated

import jwt
from jwt.exceptions import InvalidTokenError

from fastapi import Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer

from config import settings
from schemas import TokenData, UserPostDTO
from logger import Logger


oauth2_scheme = OAuth2PasswordBearer("auth/token")


def get_token(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    return token


def get_token_data(token: Annotated[str, Depends(get_token)]) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.PUBLIC_KEY, algorithms=[settings.ALGORITHM])
        sub = payload.get("sub")
        if sub is None:
            raise credentials_exception
        token_data = TokenData(id=sub)
    except InvalidTokenError as ex:
        Logger.error(f"InvalidTokenError: {ex}")
        raise credentials_exception
    Logger.info(f"User's <id: {token_data.id}> token was verified")
    return token_data


def get_user_post_form(username: Annotated[str, Form()], email: Annotated[str, Form()]) -> UserPostDTO:
    user = UserPostDTO(
        username=username,
        email=email,
    )
    return user
