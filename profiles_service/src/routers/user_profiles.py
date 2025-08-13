from typing import Annotated

from fastapi.routing import APIRouter
from fastapi import Body, Depends, HTTPException

from . import images, profile_pictures, stacks
from schemas import ProfilesPostDTO, UsersPostDTO
from dependencies import UserId


router = APIRouter(
    prefix="/user-profiles",
    tags=["user-profiles"],
    responses={404: {"description": "User profile not found"}},
)
router.include_router(images.router)
router.include_router(profile_pictures.router)
router.include_router(stacks.router)


@router.post(path="")
async def create_profile(user_id: UserId, user_data: Annotated[UsersPostDTO, Body()]):
    ...


@router.get(path="", response_model=ProfilesPostDTO)
async def get_profile(user_id: UserId):
    ...


@router.put(path="")
async def update_profile(user_id: UserId, new_user_data: Annotated[UsersPostDTO, Body()]):
    ...


@router.delete(path="")
async def delete_profile(user_id: UserId):
    ...
