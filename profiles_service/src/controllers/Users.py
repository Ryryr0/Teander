from interfaces import IUsersDB, IUsers
from schemas import UsersPostDTO, UsersDTO
from logger import Logger


class Users(IUsers):
    def __init__(self, user_db: IUsersDB):
        self.users_db = user_db

    async def get_user(self, user_id: int):
        return await self.users_db.get_user_by_id(user_id)

    async def create_user(self, user_data: UsersPostDTO) -> bool:
        if not await self.users_db.create_user(user_data):
            return False
        Logger.info(f"User <{user_data.username}> was created")
        return True

    async def update_user(self, user_id: int, new_user_data: UsersPostDTO) -> bool:
        if not await self.users_db.update_user_by_id(user_id, new_user_data):
            return False
        Logger.info(f"User <id: {user_id}> was updated")
        return True

    async def delete_user(self, user_id: int) -> bool:
        if not await self.users_db.delete_user_by_id(user_id):
            return False
        Logger.info(f"User <id: {user_id}> was deleted")
        return True
