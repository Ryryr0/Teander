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
    async def update_user_by_id(self, user_id: int, new_user_data: UsersPostDTO) -> bool:
        ...

    @abstractmethod
    async def delete_user_by_id(self, user_id) -> bool:
        ...


class IUsers(ABC):
    @abstractmethod
    async def create_user(self) -> bool:
        ...

    @abstractmethod
    async def update_user(self) -> bool:
        ...

    @abstractmethod
    async def delete_user(self) -> bool:
        ...

    @abstractmethod
    async def get_user(self) -> UsersPostDTO:
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


class IImages(ABC):
    @abstractmethod
    async def get_user_images(self, user_id: int) -> list[ImagesPostDTO]:
        ...

    @abstractmethod
    async def save_user_image(self, image: Image.Image, user_id) -> bool:
        ...

    @abstractmethod
    async def delete_user_images(self, /, image_id: int | None = None, image_ids: list[int] | None = None) -> bool:
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
