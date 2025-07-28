from abc import ABC, abstractmethod

from schemas import UserPostDTO, UserDTO


class IUserDB(ABC):
    @abstractmethod
    async def create_user(self, new_user: UserPostDTO) -> bool:
        ...

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> UserDTO | None:
        ...

    @abstractmethod
    async def update_user_by_id(self, user_id: int, new_user_data: UserPostDTO) -> bool:
        ...

    @abstractmethod
    async def delete_user_by_id(self, user_id) -> bool:
        ...
