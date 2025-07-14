from jwt.exceptions import InvalidTokenError
from typing import Annotated
import jwt

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status, Form

from config import settings
from schemas import TokenData, UserPostDTO, UserDTO
from database.queries import Queries


def user_post_form(username: Annotated[str, Form()], email: Annotated[str, Form()]) -> UserPostDTO:
    user = UserPostDTO(
        username=username,
        email=email,
    )
    return user


async def get_current_user(token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="token"))]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.PUBLIC_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(id=user_id)
    except InvalidTokenError:
        raise credentials_exception
    user = await Queries.get_user(user_id=token_data.id)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
        current_user: Annotated[UserDTO, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
