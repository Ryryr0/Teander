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
        self.users = users
        self.images = images
        self.profile_pictures = profile_pictures
        self.profile_cacher = profile_cacher

    async def create_profile(self, user_id: int, user_data: UsersPostDTO) -> bool:
        if not await self.users.create_user(user_id, user_data):
            return False
        await self.profile_pictures.create_profile_pictures(user_id)

    async def get_profile(self, user_id: int) -> ProfilesPostDTO | None:
        # Check profile in cache
        if profile_post := await self.profile_cacher.get_profile_by_user_id(user_id) is not None:
            return profile_post

        # Taking user from db
        if user := await self.users.get_user(user_id) is None:
            return None
        profile_picture = await self.profile_pictures.get_user_profile_picture(user_id)
        images = await self.images.get_user_images(user_id)
        profile_post = ProfilesPostDTO(
            user=user,
            profile_picture=profile_picture,
            images=images,
        )
        # Cache profile
        if await self.profile_cacher.cache_profile(profile_post):
            Logger.info(f"Profile <username: {profile_post.user.username}> was cached")
        return profile_post

    async def get_short_profile(self, user_id: int):
        # Check profile in cache
        if profile_post := await self.profile_cacher.get_profile_by_user_id(user_id) is not None:
            return ShortProfilesDTO(**profile_post)

        # Taking user from db
        if user := await self.users.get_user(user_id) is None:
            return None
        profile_picture = await self.profile_pictures.get_user_profile_picture(user_id)
        profile_post = ProfilesPostDTO(
            user=user,
            profile_picture=profile_picture,
        )
        # Cache profile
        if await self.profile_cacher.cache_profile(user_id, profile_post):
            Logger.info(f"Profile <username: {profile_post.user.username}> was cached")
        return profile_post

    async def update_profile(self, user_id: int, new_user_data: UsersPostDTO) -> bool:
        await self.profile_cacher.delete_cache(user_id)
        if not await self.users.update_user(user_id, new_user_data):
            return False
        Logger.info(f"User <id: {user_id}> was updated")
        return True

    async def delete_profile(self, user_id: int) -> bool:
        await self.profile_cacher.delete_cache(user_id)
        if not await self.users.delete_user(user_id):
            return False
        Logger.info(f"User <id: {user_id}> was deleted")
        return True

    async def add_image(self, image: Image.Image, user_id) -> bool:
        await self.profile_cacher.delete_cache(user_id)
        if not self.images.save_user_image(image, user_id):
            return False
        Logger.info(f"Image was added from user <id: {user_id}>")
        return True

    async def delete_profile_picture(self, user_id: int) -> bool:
        await self.profile_cacher.delete_cache(user_id)
        if not await self.profile_pictures.delete_user_profile_picture(user_id):
            return False
        Logger.info(f"Profile picture was deleted from user <id: {user_id}>")
        return True

    async def add_profile_picture(self, image: Image.Image, user_id) -> bool:
        await self.profile_cacher.delete_cache(user_id)
        if not await self.profile_pictures.save_user_profile_picture(image, user_id):
            return False
        Logger.info(f"Profile picture was added from user <id: {user_id}>")
        return True

    async def delete_image(self, image_id: int, user_id: int) -> bool:
        await self.profile_cacher.delete_cache(user_id)
        if not await self.images.delete_user_images(image_id):
            return False
        Logger.info(f"Image was deleted from user <id: {user_id}>")
        return True

    async def set_profile_picture(self, image_id: int, user_id: int):
        await self.profile_cacher.delete_cache(user_id)
        if not await self.profile_pictures.set_user_profile_picture(image_id, user_id):
            return False
        return True
