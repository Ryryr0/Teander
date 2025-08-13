from typing import Annotated

import jwt
from jwt import InvalidTokenError
from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from config import settings
from schemas import Token, TokenData
from logger import Logger


oauth_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def get_user_id(token: Annotated[str, Depends(oauth_scheme)]) -> int:
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
    return token_data.id


UserId = Annotated[int, Depends(get_user_id)]
