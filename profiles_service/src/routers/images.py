from typing import Annotated

from fastapi.routing import APIRouter
from fastapi import UploadFile, Path

from schemas import ImagesPostDTO
from dependencies import UserId


router = APIRouter(
    prefix="/images",
    tags=["images"],
    responses={404: {"description": "Images not found"}},
)


@router.post(path="")
async def add_image(user_id: UserId, image: UploadFile):
    ...


@router.get(path="", response_model=list[ImagesPostDTO])
async def get_images(user_id: UserId):
    ...


@router.delete(path="/{image_id}")
async def delete_image(user_id: UserId, image_id: Annotated[int, Path()]):
    ...
