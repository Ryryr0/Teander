from typing import Annotated

from fastapi.routing import APIRouter
from fastapi import UploadFile, Path, HTTPException, status, Response

from schemas import ImagesPostDTO
from dependencies import UserId, GetImages


router = APIRouter(
    prefix="/images",
    tags=["images"],
    responses={404: {"description": "Images not found"}},
)


@router.post(path="")
async def add_image(user_id: UserId, image: UploadFile, images: GetImages):
    if not await images.save_user_image(image, user_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Image not saved",
        )
    return Response(status_code=status.HTTP_201_CREATED)


@router.delete(path="/{image_id}")
async def delete_image(user_id: UserId, image_id: Annotated[int, Path()], images: GetImages):
    if not await images.delete_user_images(image_id):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong, try again"
        )
    return Response(status_code=status.HTTP_200_OK)
