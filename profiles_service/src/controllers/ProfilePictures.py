from PIL import Image

from interfaces import IProfilePictures, IProfilePicturesDB
from schemas import ImagesPostDTO


class ProfilePictures(IProfilePictures):
    def __init__(self, profile_picture_db: IProfilePicturesDB):
        self.profile_picture_db = profile_picture_db

    async def create_profile_pictures(self, user_id: int):
        return self.profile_picture_db.create_profile_picture_for_user_id(user_id)

    async def get_user_profile_picture(self, user_id: int) -> ImagesPostDTO:
        return await self.profile_picture_db.get_profile_picture_by_user_id(user_id)

    async def set_user_profile_picture(self, image_id: int, user_id: int) -> bool:
        return await self.profile_picture_db.set_profile_picture(image_id, user_id)

    async def save_user_profile_picture(self, image: Image.Image, user_id: int) -> bool:
        return await self.profile_picture_db.save_profile_picture(image, user_id)

    async def delete_user_profile_picture(self, user_id) -> bool:
        return await self.profile_picture_db.delete_profile_picture(user_id)
