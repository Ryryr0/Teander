from typing import Annotated

from fastapi.routing import APIRouter
from fastapi import UploadFile, Path

from schemas import ImagesPostDTO
from dependencies import UserId


router = APIRouter(
    prefix="/profile-pictures",
    tags=["profile-pictures"],
    responses={404: {"description": "Profile picture not found"}},
)


@router.post(path="")
async def add_profile_picture(user_id: UserId, image: UploadFile):
    ...


@router.get(path="", response_model=ImagesPostDTO)
async def get_profile_picture(user_id: UserId):
    ...


@router.put(path="/{image_id}")
async def set_profile_picture(user_id: UserId, image_id: Annotated[int, Path()]):
    ...


@router.delete(path="")
async def delete_profile_picture(user_id: UserId):
    ...

