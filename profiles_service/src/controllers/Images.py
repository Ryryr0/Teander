from fastapi import UploadFile

from interfaces import IImages, IImagesDB
from schemas import ImagesPostDTO


class Images(IImages):
    def __init__(self, image_db: IImagesDB):
        self.__image_db = image_db

    async def get_user_images(self, user_id: int) -> list[ImagesPostDTO]:
        return await self.__image_db.get_images_by_user_id(user_id)

    async def save_user_image(self, image: UploadFile, user_id) -> bool:
        if not await self.__image_db.save_image(image, user_id):
            return False
        return True

    async def delete_user_images(self, image_id: int) -> bool:
        if not await self.__image_db.delete_image(image_id):
            return False
        return True
