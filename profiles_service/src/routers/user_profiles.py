from typing import Annotated
import httpx

from fastapi.routing import APIRouter
from fastapi import Body, Depends, HTTPException, status, Response, Request

from . import images, profile_pictures, stacks
from schemas import ProfilesPostDTO, UsersPostDTO, ShortProfilesDTO
from dependencies import UserId, GetProfile
from config import settings


router = APIRouter(
    prefix="/user-profiles",
    tags=["user-profiles"],
    responses={404: {"description": "User profile not found"}},
)
router.include_router(images.router)
router.include_router(profile_pictures.router)
router.include_router(stacks.router)


@router.post("/token")
async def get_token(request: Request):
    """Proxy to auth-service token endpoint"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            settings.AUTH_SERVICE_TOKEN,
            data=await request.form()
        )
    return response.json()


@router.get(path="", response_model=ProfilesPostDTO)
async def get_profile(user_id: UserId, profiles: GetProfile):
    if (profile := await profiles.get_profile(user_id)) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist or disabled",
        )
    return profile


@router.get(path="/short", response_model=ShortProfilesDTO)
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
