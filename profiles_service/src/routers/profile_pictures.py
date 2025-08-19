from typing import Annotated

from fastapi.routing import APIRouter
from fastapi import UploadFile, Path, HTTPException, status, Response

from schemas import ImagesPostDTO
from dependencies import UserId, GetProfilePictures


router = APIRouter(
    prefix="/profile-pictures",
    tags=["profile-pictures"],
    responses={404: {"description": "Profile picture not found"}},
)


@router.post(path="")
async def add_profile_picture(user_id: UserId, image: UploadFile, profile_pictures: GetProfilePictures):
    if image.content_type is None or not image.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image format",
        )
    if not await profile_pictures.save_user_profile_picture(image, user_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Image not saved",
        )
    return Response(status_code=status.HTTP_201_CREATED)


@router.put(path="/{image_id}")
async def set_profile_picture(user_id: UserId, image_id: Annotated[int, Path()], profile_pictures: GetProfilePictures):
    if not await profile_pictures.set_user_profile_picture(image_id, user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found",
        )
    return Response(status_code=status.HTTP_200_OK)


@router.delete(path="")
async def delete_profile_picture(user_id: UserId, profile_pictures: GetProfilePictures):
    if not await profile_pictures.delete_user_profile_picture(user_id):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong, try again"
        )

