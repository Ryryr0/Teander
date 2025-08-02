from PIL import Image

from interfaces import IProfilePictures, IImagesDB
from schemas import ImagesPostDTO


class ProfilePictures(IProfilePictures):
    def __init__(self, images_db: IImagesDB):
        self.images_db = images_db

    async def get_user_profile_picture(self, user_id: int) -> ImagesPostDTO:
        ...

    async def set_user_profile_picture(self, image_id: int, user_id: int) -> bool:
        ...

    async def save_user_profile_picture(self, image: Image.Image, user_id: int) -> bool:
        ...

    async def delete_user_profile_picture(self, user_id) -> bool:
        ...
