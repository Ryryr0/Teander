from jwt.exceptions import InvalidTokenError
from typing import Annotated
import jwt

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status, Form

from config import settings
from logger import Logger
from schemas import TokenData, UserPostDTO, UserDTO
from database.queries import Queries


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")


def get_user_post_form(username: Annotated[str, Form()], email: Annotated[str, Form()]) -> UserPostDTO:
    user = UserPostDTO(
        username=username,
        email=email,
    )
    return user


def get_token_data(jwt_token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(jwt_token, settings.PUBLIC_KEY, algorithms=[settings.ALGORITHM])
        sub = payload.get("sub")
        if sub is None:
            raise credentials_exception
        token_data = TokenData(id=sub)
    except InvalidTokenError as ex:
        Logger.error(f"InvalidTokenError: {ex}")
        raise credentials_exception
    Logger.info(f"User's <id: {token_data.id}> token was verified")
    return token_data


# async def get_current_user(token_data: Annotated[TokenData, Depends(get_token_data)]):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     user = await Queries.get_user(user_id=token_data.id)
#     if user is None:
#         raise credentials_exception
#     return user
#
#
# async def get_current_active_user(
#         current_user: Annotated[UserDTO, Depends(get_current_user)],
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user
