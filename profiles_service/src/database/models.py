from sqlalchemy import select, or_
from sqlalchemy.exc import IntegrityError

from interfaces import IUserDB
from schemas import UserPostDTO, UserDTO
from .database import async_session_factory
from ORM_models import UsersOrm
from logger import Logger


class UserDB(IUserDB):
    async def create_user(self, new_user: UserPostDTO):
        async with async_session_factory() as session:
            try:
                if await UserDB.__check_duplication_user(new_user):
                    session.add(UsersOrm(**new_user.model_dump()))
                else:
                    return False
            except IntegrityError as ex:
                await session.rollback()
                Logger.error(f"DataBase IntegrityError: {ex}")
                return False
            await session.commit()
        return True

    async def get_user_by_id(self, user_id: int) -> UserDTO | None:
        async with async_session_factory() as session:
            try:
                user_orm = await session.get(UsersOrm, user_id)
            except IntegrityError as ex:
                await session.rollback()
                Logger.error(f"DataBase IntegrityError: {ex}")
                return None
            await session.commit()

        if user_orm:
            user = UserDTO.model_validate(user_orm, from_attributes=True)
        else:
            user = None
        return user

    async def update_user_by_id(self, user_id: int, new_user_data: UserPostDTO) -> bool:
        async with async_session_factory() as session:
            try:
                if await UserDB.__check_duplication_user(new_user_data):
                    user_orm = await session.get(UsersOrm, user_id)
                else:
                    return False
                if user_orm:
                    for attr, value in new_user_data.model_dump().items():
                        setattr(user_orm, attr, value)
                else:
                    return False
            except IntegrityError as ex:
                await session.rollback()
                Logger.error(f"DataBase IntegrityError: {ex}")
                return False
            await session.commit()
        return True

    async def delete_user_by_id(self, user_id: int) -> bool:
        async with async_session_factory() as session:
            try:
                user = await session.get(UsersOrm, user_id)
                user.disabled = True
            except IntegrityError as ex:
                await session.rollback()
                Logger.error(f"DataBase IntegrityError: {ex}")
                return False
            await session.commit()
        return True

    @staticmethod
    async def __check_duplication_user(user: UserPostDTO) -> bool:
        query = (
            select(
                UsersOrm.username,
                UsersOrm.email,
            )
            .select_from(UsersOrm)
            .filter(or_(
                UsersOrm.username == user.username,
                UsersOrm.email == user.email,
            ))
        )

        async with async_session_factory() as session:
            try:
                exec_result = await session.execute(query)
                results = exec_result.all()
                if not results:
                    return False
            except IntegrityError as ex:
                await session.rollback()
                Logger.error(f"DataBase IntegrityError: {ex}")
                return False
            await session.commit()
        return True
