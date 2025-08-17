from database.models import UsersDB
from interfaces import IUsers, IUsersDB
from schemas import UsersDTO, UsersPostDTO
from logger import Logger


class Users(IUsers):
    def __init__(self, users_db: IUsersDB, synchronizer: ):
        self.users_db = users_db
        self.synchronizer = synchronizer

    async def create_user(self, new_user: UsersPostDTO, hashed_password: str) -> bool:
        if not await self.users_db.create_user(new_user, hashed_password):
            return False
        Logger.info(f"User <username: {new_user.username} created>")

        return True

    async def get_user(self, username: str) -> UsersDTO | None:
        return await self.users_db.get_user_by_username(username)

    async def update_user(self, new_user_date: UsersPostDTO) -> bool:
        ...

    async def update_password(self, user_id: int, new_hashed_password: str) -> bool:
        ...