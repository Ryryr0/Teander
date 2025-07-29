from abc import ABC, abstractmethod

from schemas import UsersPostDTO, UsersDTO


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
    @property
    @abstractmethod
    async def userdata(self) -> UsersPostDTO:
        ...

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

    @abstractmethod
    async def get_user_images(self):
        ...
