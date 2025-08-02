from abc import ABC, abstractmethod

from PIL import Image

from schemas import UsersPostDTO, UsersDTO, ImagesPostDTO


class IUsersDB(ABC):
    @abstractmethod
    async def create_user(self, new_user: UsersPostDTO) -> bool:
        ...

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> UsersDTO | None:
        ...

    @abstractmethod
    async def update_user_by_id(self, user_id: int, new_user_data: UsersDTO) -> bool:
        ...

    @abstractmethod
    async def delete_user_by_id(self, user_id) -> bool:
        ...


class IUsers(ABC):
    @property
    @abstractmethod
    async def user_data(self) -> UsersDTO:
        ...

    @classmethod
    @abstractmethod
    async def create_user(cls, users_db: IUsersDB, user_data: UsersPostDTO) -> bool:
        """Create user in db"""
        ...

    @classmethod
    @abstractmethod
    def create_instance(cls, user_db: IUsersDB, user_id: int, user_data: UsersPostDTO):
        """Create instance of class Users"""
        ...

    @classmethod
    @abstractmethod
    async def get_user(cls, users_db: IUsersDB, user_id: int):
        """Get user from db by id"""
        ...

    @abstractmethod
    async def update_user(self) -> bool:
        """Update user in db"""
        ...

    @abstractmethod
    async def delete_user(self) -> bool:
        """Delete user in db"""
        ...

    @abstractmethod
    def get_post_user(self) -> UsersPostDTO:
        """Get data class UsersPostDTO"""
        ...


class IImagesDB(ABC):
    @abstractmethod
    async def save_image(self, image: Image.Image, user_id: int) -> bool:
        ...

    @abstractmethod
    async def get_images_by_user_id(self, user_id: int) -> list[ImagesPostDTO]:
        ...

    @abstractmethod
    async def delete_image(self, image_id: int) -> bool:
        ...


class IImagesStorage(ABC):
    @abstractmethod
    async def save_image(self, image: Image.Image) -> str:
        ...

    @abstractmethod
    async def delete_image(self, image_id: int) -> bool:
        ...


class IImages(ABC):
    @abstractmethod
    async def get_user_images(self, user_id: int) -> list[ImagesPostDTO]:
        ...

    @abstractmethod
    async def save_user_image(self, image: Image.Image, user_id) -> bool:
        ...

    @abstractmethod
    async def delete_user_images(self, image_id: int) -> bool:
        ...


class IProfilePicturesDB(ABC):
    @abstractmethod
    async def get_profile_picture_by_user_id(self, user_id: int) -> ImagesPostDTO | None:
        ...

    @abstractmethod
    async def save_profile_picture(self, image: Image.Image, user_id: int) -> bool:
        ...

    @abstractmethod
    async def set_profile_picture(self, image_id: int, user_id: int) -> bool:
        ...


class IProfilePictures(ABC):
    @abstractmethod
    async def get_user_profile_picture(self, user_id: int) -> ImagesPostDTO:
        ...

    @abstractmethod
    async def save_user_profile_picture(self, image: Image.Image, user_id: int) -> bool:
        ...

    @abstractmethod
    async def set_user_profile_picture(self, image_id: int, user_id: int) -> bool:
        ...

    @abstractmethod
    async def delete_user_profile_picture(self, user_id) -> bool:
        ...
