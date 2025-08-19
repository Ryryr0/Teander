from typing import Annotated

import jwt
from jwt import InvalidTokenError
from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from config import settings
from schemas import Token, TokenData
from logger import Logger
from controllers import Profiles, Users, ProfilePictures, Images
from database.models import UsersDB, ImagesDB, ProfilePicturesDB, ImagesStorage
from database.cachers import ProfileCacher
from database.database import async_session_factory
from interfaces import IProfiles, IProfilePictures, IImages

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


def create_profiles_controller() -> IProfiles:
    # DB models creation
    users_db = UsersDB(async_session_factory)
    images_storage = ImagesStorage()
    images_db = ImagesDB(async_session_factory, images_storage)
    profile_pictures_db = ProfilePicturesDB(async_session_factory, images_storage)
    profile_cacher = ProfileCacher()

    # Controllers creation
    users = Users(users_db)
    images = Images(images_db)
    profile_pictures = ProfilePictures(profile_pictures_db)

    profiles = Profiles(
        users=users,
        images=images,
        profile_pictures=profile_pictures,
        profile_cacher=profile_cacher,
    )
    return profiles


def create_profile_pictures_controller() -> IProfilePictures:
    images_storage = ImagesStorage()
    profile_pictures_db = ProfilePicturesDB(async_session_factory, images_storage)
    return ProfilePictures(profile_pictures_db)


def create_images_controller() -> IImages:
    images_storage = ImagesStorage()
    images_db = ImagesDB(async_session_factory, images_storage)
    return Images(images_db)


# Commonly used types
UserId = Annotated[int, Depends(get_user_id)]
GetProfile = Annotated[IProfiles, Depends(create_profiles_controller)]
GetProfilePictures = Annotated[IProfilePictures, Depends(create_profile_pictures_controller)]
GetImages = Annotated[Images, Depends(create_images_controller)]
