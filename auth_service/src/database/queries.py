from typing import Any

from sqlalchemy import select, or_
from sqlalchemy.exc import IntegrityError

from .database import async_session_factory, async_engine, Base
from .models import UsersOrm
from schemas import UserDTO

import asyncio


# temporary
async def insert_users():
    async with async_session_factory() as session:
        users = [
            UsersOrm(username="Bobr",
                     email="artemkoral@gmail.com", hashed_password="adasdfaa", disabled=False),
            UsersOrm(username="Volk",
                     email="tomsoer@gmail.com", hashed_password="adasdsdfsdffaa", disabled=True),
            UsersOrm(username="Cookie",
                     email="shastynec@gmail.com", hashed_password="ahshajhdaadasdad", disabled=False),
            UsersOrm(username="Evilmore",
                     email="badguy@gmail.com", hashed_password="klxklkplxcmvxm", disabled=False),
            UsersOrm(username="God",
                     email="foxpaw@gmail.com", hashed_password="ytreqbbxcm", disabled=False),
            UsersOrm(username="Zar",
                     email="petrperv@gmail.com", hashed_password="kiouoimklnlj", disabled=True),
        ]
        session.add_all(users)
        await session.commit()


async def create_tables():  # need to shift in database (mb)
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await insert_users()
    print(await Queries.get_user(10))


class Queries:
    @staticmethod
    async def get_user(user_id: int | None = None, username: str | None = None) -> UserDTO | None:
        """
        Only id or username
        """
        if user_id:
            get_by = user_id
        elif username:
            get_by = username
        else:
            return None

        async with async_session_factory() as session:
            try:
                user_db = await session.get(UsersOrm, get_by)
                if not user_db:
                    raise ValueError(f"User with {get_by} not found")
            except ValueError as ex:
                # there could be logs
                await session.rollback()

        if user_db:
            user_dto = UserDTO.model_validate(user_db, from_attributes=True)
        else:
            user_dto = None
        return user_dto

    @staticmethod
    async def update_user(new_user_data: UserDTO) -> bool:
        async with async_session_factory() as session:
            try:
                if await Queries.__check_duplication_user_data(new_user_data):
                    user_orm = await session.get(UsersOrm, new_user_data.id)
                if not user_orm:
                    raise ValueError(f"User <{new_user_data}> doesn't exist")
                for key, item in new_user_data.model_dump().items():
                    setattr(user_orm, key, item)
            except IntegrityError as ex:
                await session.rollback()
                raise ValueError(f"User already exist or incorrect data: {ex.detail}")
            await session.commit()
        await Queries.__synchronize_db()
        return True

    @staticmethod
    async def post_user(user: UserDTO) -> bool:
        async with async_session_factory() as session:
            try:
                if await Queries.__check_duplication_user_data(user):
                    session.add(UsersOrm(**user.model_dump()))

            except IntegrityError as ex:
                await session.rollback()
                raise ValueError(f"User already exist or incorrect data: {ex.detail}")

            await session.commit()
        await Queries.__synchronize_db()
        return True

    @staticmethod
    async def __check_duplication_user_data(user: UserDTO) -> bool:
        async with async_session_factory() as session:
            try:
                query = (
                    select(
                        UsersOrm.username,
                        UsersOrm.email,
                        UsersOrm.disabled,
                    )
                    .select_from(UsersOrm)
                    .filter(or_(
                        UsersOrm.username == user.username,
                        UsersOrm.email == user.email,
                    ))
                )
                res = await session.execute(query)
                result = res.all()

                for record in result:
                    if (user.username in record) and not record[2]:
                        raise ValueError("Username is already used")
                    elif (user.email in record) and not record[2]:
                        raise ValueError("Email is already used")
            except IntegrityError as ex:
                raise ValueError(f"User already exist or incorrect data: {ex.detail}")
        return True

    @staticmethod
    async def __synchronize_db():  # synchronization of the auth-service's db with the others services' dbs
        pass


# asyncio.run(create_tables())
