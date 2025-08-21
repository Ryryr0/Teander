from abc import ABC, abstractmethod

from fastapi import UploadFile
from schemas import UsersPostDTO, UsersDTO, ImagesPostDTO, ProfilesPostDTO, ShortProfilesDTO


class IUsersDB(ABC):
    @abstractmethod
    async def create_user(self, user_id: int, new_user: UsersPostDTO) -> bool:
        ...

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> UsersDTO | None:
        ...

    @abstractmethod
    async def update_user_by_id(self, user_id: int, new_user_data: UsersPostDTO, allow_main_data_changes: bool = False) -> bool:
        ...

    @abstractmethod
    async def delete_user_by_id(self, user_id: int) -> bool:
        ...


class IUsers(ABC):
    @abstractmethod
    async def create_user(self, user_id: int, user_data: UsersPostDTO) -> bool:
        """Create user in db"""
        ...

    @abstractmethod
    async def get_user(self, user_id: int) -> UsersPostDTO | None:
        """Get user from db by id"""
        ...

    @abstractmethod
    async def update_user(self, user_id: int, new_user_data: UsersPostDTO, allow_main_data_changes: bool = False) -> bool:
        """Update user in db"""
        ...

    @abstractmethod
    async def delete_user(self, user_id: int) -> bool:
        """Delete user in db"""
        ...


class IImagesDB(ABC):
    @abstractmethod
    async def save_image(self, image: UploadFile, user_id: int) -> bool:
        ...

    @abstractmethod
    async def get_images_by_user_id(self, user_id: int) -> list[ImagesPostDTO]:
        ...

    @abstractmethod
    async def delete_image(self, image_id: int) -> bool:
        ...


class IImagesStorage(ABC):
    @abstractmethod
    async def save_image(self, image: UploadFile) -> str:
        ...

    @abstractmethod
    async def delete_image(self, image_id: int) -> bool:
        ...


class IImages(ABC):
    @abstractmethod
    async def get_user_images(self, user_id: int) -> list[ImagesPostDTO]:
        ...

    @abstractmethod
    async def save_user_image(self, image: UploadFile, user_id: int) -> bool:
        ...

    @abstractmethod
    async def delete_user_images(self, image_id: int) -> bool:
        ...


class IProfilePicturesDB(ABC):
    @abstractmethod
    async def create_profile_picture_for_user_id(self, user_id: int) -> bool:
        ...

    @abstractmethod
    async def get_profile_picture_by_user_id(self, user_id: int) -> ImagesPostDTO | None:
        ...

    @abstractmethod
    async def save_profile_picture(self, image: UploadFile, user_id: int) -> bool:
        ...

    @abstractmethod
    async def set_profile_picture(self, image_id: int, user_id: int) -> bool:
        ...

    @abstractmethod
    async def delete_profile_picture(self, user_id: int) -> bool:
        ...


class IProfilePictures(ABC):
    @abstractmethod
    async def create_profile_pictures(self, user_id: int) -> bool:
        ...

    @abstractmethod
    async def get_user_profile_picture(self, user_id: int) -> ImagesPostDTO | None:
        ...

    @abstractmethod
    async def save_user_profile_picture(self, image: UploadFile, user_id: int) -> bool:
        ...

    @abstractmethod
    async def set_user_profile_picture(self, image_id: int, user_id: int) -> bool:
        ...

    @abstractmethod
    async def delete_user_profile_picture(self, user_id: int) -> bool:
        ...


class IProfilesCacher(ABC):
    @abstractmethod
    async def get_profile_by_user_id(self, user_id: int) -> ProfilesPostDTO | None:
        ...

    @abstractmethod
    async def cache_profile(self, user_id: int, profile: ProfilesPostDTO) -> bool:
        ...

    @abstractmethod
    async def delete_cache(self, user_id: int) -> bool:
        ...


class IProfiles(ABC):
    @abstractmethod
    async def create_profile(self, user_id: int, user_data: UsersPostDTO) -> bool:
        ...

    @abstractmethod
    async def get_profile(self, user_id: int) -> ProfilesPostDTO | None:
        ...

    @abstractmethod
    async def get_short_profile(self, user_id: int) -> ShortProfilesDTO | None:
        ...

    @abstractmethod
    async def update_profile(self, user_id: int, new_user_data: UsersPostDTO) -> bool:
        ...

    @abstractmethod
    async def delete_profile(self, user_id: int) -> bool:
        ...

    
class ISynchronizer(ABC):
    @abstractmethod
    async def start(self):
        ...
