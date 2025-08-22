from fastapi import UploadFile

from interfaces import IImages, IImagesDB, ICacheCleaner
from schemas import ImagesPostDTO


class Images(IImages):
    def __init__(self, image_db: IImagesDB, cache_cleaner: ICacheCleaner):
        self.__image_db = image_db
        self.__cache_cleaner = cache_cleaner

    async def get_user_images(self, user_id: int) -> list[ImagesPostDTO]:
        return await self.__image_db.get_images_by_user_id(user_id)

    async def save_user_image(self, image: UploadFile, user_id) -> bool:
        if not await self.__image_db.save_image(image, user_id):
            return False
        await self.__cache_cleaner.delete_cache(user_id)
        return True

    async def delete_user_images(self, image_id: int, user_id: int) -> bool:
        if not await self.__image_db.delete_image(image_id, user_id):
            return False
        await self.__cache_cleaner.delete_cache(user_id)
        return True
