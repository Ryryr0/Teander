from typing import Annotated

from fastapi.routing import APIRouter
from fastapi import Body, Depends, HTTPException, status, Response

from . import images, profile_pictures, stacks
from schemas import ProfilesPostDTO, UsersPostDTO
from dependencies import UserId, GetProfile


router = APIRouter(
    prefix="/user-profiles",
    tags=["user-profiles"],
    responses={404: {"description": "User profile not found"}},
)
router.include_router(images.router)
router.include_router(profile_pictures.router)
router.include_router(stacks.router)


@router.post(path="")
async def create_profile(
        user_id: UserId,
        user_data: Annotated[UsersPostDTO, Body()],
        profiles: GetProfile,
):
    if not await profiles.create_profile(user_id, user_data):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="User already exist or wrong data",
        )
    return Response(status_code=status.HTTP_201_CREATED)


@router.get(path="", response_model=ProfilesPostDTO)
async def get_profile(user_id: UserId, profiles: GetProfile):
    if (profile := await profiles.get_profile(user_id)) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist or disabled",
        )
    return profile


@router.get(path="/short", response_model=ProfilesPostDTO)
async def get_short_profile(user_id: UserId, profiles: GetProfile):
    if (short_profile := await profiles.get_short_profile(user_id)) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist or disabled",
        )
    return short_profile


@router.put(path="")
async def update_profile(
        user_id: UserId,
        new_user_data: Annotated[UsersPostDTO, Body()],
        profiles: GetProfile,
):
    if not await profiles.update_profile(user_id, new_user_data):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Wrong data",
        )
    return Response(status_code=status.HTTP_200_OK)


@router.delete(path="")
async def delete_profile(user_id: UserId, profiles: GetProfile):
    if not await profiles.delete_profile(user_id):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong, try again",
        )
    return Response(status_code=status.HTTP_200_OK)
