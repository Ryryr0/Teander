from interfaces import IUsersDB, IUsers
from schemas import UsersPostDTO, UsersDTO
from logger import Logger


class Users(IUsers):
    def __init__(self, user_db: IUsersDB, user_data: UsersDTO):
        self.users_db = user_db
        self.user_data = user_data

    @classmethod
    async def get_user(cls, users_db: IUsersDB, user_id: int):
        user_data = await users_db.get_user_by_id(user_id)
        return cls(users_db, user_data)

    @classmethod
    async def create_user(cls, users_db: IUsersDB, user_data: UsersPostDTO) -> bool:
        if not await users_db.create_user(user_data):
            return False
        Logger.info(f"User <{user_data.username}> was created")
        return True

    @classmethod
    def create_instance(cls, user_db: IUsersDB, user_id: int, user_post_data: UsersPostDTO):
        user_data = UsersDTO(id=user_id, **user_post_data.model_dump())
        return cls(user_db, user_data)

    @property
    def user_data(self) -> UsersDTO:
        return self.user_data

    @user_data.setter
    def user_data(self, value: UsersDTO):
        self._user_data = value

    async def update_user(self) -> bool:
        if not await self.users_db.update_user_by_id(self.user_data.id, self.user_data):
            return False
        Logger.info(f"User <id: {self.user_data.id}, username: {self.user_data.username}> was updated")
        return True

    async def delete_user(self) -> bool:
        if not await self.users_db.delete_user_by_id(self.user_data.id):
            return False
        Logger.info(f"User <id: {self.user_data.id}, username: {self.user_data.username}> was deleted")
        return True

    def get_post_user(self) -> UsersPostDTO:
        return UsersPostDTO(**self.user_data.model_dump())

