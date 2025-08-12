import itertools

from PIL import Image

from interfaces import IUsersDB, IProfilePicturesDB, IImagesDB, IProfilesCacher
from schemas import UsersPostDTO, UsersDTO, ImagesPostDTO, ProfilesPostDTO


class FakeUsersDB(IUsersDB):
    def __init__(self):
        self._users: dict[int, UsersDTO] = {}

    async def create_user(self, user_id: int, new_user: UsersPostDTO) -> bool:
        if (
                user_id in self._users or
                new_user in [UsersPostDTO(**user.model_dump()) for user in self._users.values()]
        ):
            return False
        self._users[user_id] = UsersDTO(**new_user.model_dump(), id=user_id, disabled=False)
        return True

    async def get_user_by_id(self, user_id: int) -> UsersDTO | None:
        return self._users.get(user_id)

    async def update_user_by_id(self, user_id: int, new_user_data: UsersPostDTO) -> bool:
        if user_id not in self._users:
            return False
        existing_user = self._users[user_id]
        self._users[user_id] = UsersDTO(
            id=existing_user.id,
            username=existing_user.username,
            email=existing_user.email,
            full_name=new_user_data.full_name,
            gender=new_user_data.gender,
            birthday=new_user_data.birthday,
            zodiac_sign=new_user_data.zodiac_sign,
            description=new_user_data.description,
            disabled=existing_user.disabled
        )
        return True

    async def delete_user_by_id(self, user_id: int) -> bool:
        return self._users.pop(user_id, None) is not None


class FakeImagesDB(IImagesDB):
    def __init__(self):
        self._images: dict[int, ImagesPostDTO] = {}
        self._id_counter = itertools.count(1)

    async def save_image(self, image: Image.Image, user_id: int) -> bool:
        try:
            new_id = next(self._id_counter)
            img_dto = ImagesPostDTO(id=new_id, url=f"http://testserver/images/{new_id}")
            self._images[new_id] = img_dto
            return True
        except Exception:
            return False

    async def get_images_by_user_id(self, user_id: int) -> list[ImagesPostDTO]:
        return [dto for _, dto in self._images.items()]

    async def delete_image(self, image_id: int) -> bool:
        print("del", self._images)
        return self._images.pop(image_id, None) is not None


class FakeProfilePicturesDB(IProfilePicturesDB):
    def __init__(self, images_db: IImagesDB):
        self._profile_pictures: dict[int, int | None] = {}
        self._images_db = images_db
        self._id_counter = itertools.count(1)

    async def create_profile_picture_for_user_id(self, user_id: int) -> bool:
        if user_id in self._profile_pictures:
            return False
        self._profile_pictures[user_id] = None
        return True

    async def get_profile_picture_by_user_id(self, user_id: int) -> ImagesPostDTO | None:
        image_id = self._profile_pictures.get(user_id)
        if image_id is None:
            return None
        images = await self._images_db.get_images_by_user_id(user_id)
        for img in images:
            if img.id == image_id:
                return img
        return None

    async def save_profile_picture(self, image: Image.Image, user_id: int) -> bool:
        success = await self._images_db.save_image(image, user_id)
        if not success:
            return False
        # Get latest saved image
        images = await self._images_db.get_images_by_user_id(user_id)
        latest_image = max(images, key=lambda img: img.id)
        self._profile_pictures[user_id] = latest_image.id
        return True

    async def set_profile_picture(self, image_id: int, user_id: int) -> bool:
        images = await self._images_db.get_images_by_user_id(user_id)
        if not any(img.id == image_id for img in images):
            return False
        self._profile_pictures[user_id] = image_id
        return True

    async def delete_profile_picture(self, user_id: int) -> bool:
        if user_id not in self._profile_pictures:
            return False
        self._profile_pictures[user_id] = None
        return True


class FakeProfilesCacher(IProfilesCacher):
    def __init__(self):
        self._cache: dict[int, ProfilesPostDTO] = {}

    async def get_profile_by_user_id(self, user_id: int) -> ProfilesPostDTO | None:
        return self._cache.get(user_id)

    async def cache_profile(self, user_id: int, profile: ProfilesPostDTO) -> bool:
        self._cache[user_id] = profile
        return True

    async def delete_cache(self, user_id: int) -> bool:
        if user_id in self._cache:
            del self._cache[user_id]
            return True
        return False

