from PIL import Image

from interfaces import IProfiles, IProfilesCacher, IUsers, IProfilePictures, IImages
from schemas import ProfilesPostDTO, UsersPostDTO, ShortProfilesDTO, ImagesPostDTO
from logger import Logger


class Profiles(IProfiles):
    def __init__(
            self,
            users: IUsers,
            images: IImages,
            profile_pictures: IProfilePictures,
            profile_cacher: IProfilesCacher
    ):
        self.__users = users
        self.__images = images
        self.__profile_pictures = profile_pictures
        self.__profile_cacher = profile_cacher

    async def create_profile(self, user_id: int, user_data: UsersPostDTO) -> bool:
        if not await self.__users.create_user(user_id, user_data):
            return False
        Logger.info(f"Profile <id: {user_id}> was created")
        return await self.__profile_pictures.create_profile_pictures(user_id)

    async def get_profile(self, user_id: int) -> ProfilesPostDTO | None:
        # Check profile in cache
        if (profile_post := await self.__profile_cacher.get_profile_by_user_id(user_id)) is not None:
            return profile_post

        # Taking user from db
        if (user := await self.__users.get_user(user_id)) is None:
            return None
        profile_picture = await self.__profile_pictures.get_user_profile_picture(user_id)
        images = await self.__images.get_user_images(user_id)
        profile_post = ProfilesPostDTO(
            user=user,
            profile_picture=profile_picture,
            images=images,
        )
        # Cache profile
        if await self.__profile_cacher.cache_profile(user_id, profile_post):
            Logger.info(f"Profile <id: {user_id}> was cached")
        return profile_post

    async def get_short_profile(self, user_id: int):
        # Check profile in cache
        if (profile_post := await self.__profile_cacher.get_profile_by_user_id(user_id)) is not None:
            return ShortProfilesDTO(**profile_post.model_dump())

        # Taking user from db
        if user := await self.__users.get_user(user_id) is None:
            return None
        profile_picture = await self.__profile_pictures.get_user_profile_picture(user_id)
        profile_post = ProfilesPostDTO(
            user=user,
            profile_picture=profile_picture,
        )
        # Cache profile
        if await self.__profile_cacher.cache_profile(user_id, profile_post):
            Logger.info(f"Short profile <id: {id}> was cached")
        return profile_post

    async def update_profile(self, user_id: int, new_user_data: UsersPostDTO) -> bool:
        await self.__profile_cacher.delete_cache(user_id)
        if not await self.__users.update_user(user_id, new_user_data):
            return False
        Logger.info(f"Profile <id: {user_id}> was updated")
        return True

    async def delete_profile(self, user_id: int) -> bool:
        await self.__profile_cacher.delete_cache(user_id)
        if not await self.__users.delete_user(user_id):
            return False
        Logger.info(f"Profile <id: {user_id}> was deleted")
        return True

    async def add_image(self, image: Image.Image, user_id) -> bool:
        await self.__profile_cacher.delete_cache(user_id)
        if not await self.__images.save_user_image(image, user_id):
            return False
        Logger.info(f"Image was added for user <id: {user_id}>")
        return True

    async def delete_profile_picture(self, user_id: int) -> bool:
        await self.__profile_cacher.delete_cache(user_id)
        if not await self.__profile_pictures.delete_user_profile_picture(user_id):
            return False
        Logger.info(f"Profile picture was deleted from user <id: {user_id}>")
        return True

    async def add_profile_picture(self, image: Image.Image, user_id) -> bool:
        await self.__profile_cacher.delete_cache(user_id)
        if not await self.__profile_pictures.save_user_profile_picture(image, user_id):
            return False
        Logger.info(f"Profile picture was added for user <id: {user_id}>")
        return True

    async def delete_image(self, image_id: int, user_id: int) -> bool:
        await self.__profile_cacher.delete_cache(user_id)
        if not await self.__images.delete_user_images(image_id):
            return False
        Logger.info(f"Image was deleted from user <id: {user_id}>")
        return True

    async def set_profile_picture(self, image_id: int, user_id: int):
        await self.__profile_cacher.delete_cache(user_id)
        if not await self.__profile_pictures.set_user_profile_picture(image_id, user_id):
            return False
        Logger.info(f"Image <id: {image_id}> was set as profile picture for user <id: {user_id}>")
        return True
