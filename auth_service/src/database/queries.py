from typing import Any
import json
import asyncio

from sqlalchemy import select, or_
from sqlalchemy.exc import IntegrityError
from aiokafka import AIOKafkaProducer
from fastapi.encoders import jsonable_encoder

from logger import Logger
from .database import async_session_factory
from .models import UsersOrm
from schemas import UserDTO, UserSendDTO, UserPostDTO


# temporary
# async def insert_users():
#     async with async_session_factory() as session:
#         users = [
#             UsersOrm(username="Bobr",
#                      email="artemkoral@gmail.com", hashed_password="adasdfaa", disabled=False),
#             UsersOrm(username="Volk",
#                      email="tomsoer@gmail.com", hashed_password="adasdsdfsdffaa", disabled=True),
#             UsersOrm(username="Cookie",
#                      email="shastynec@gmail.com", hashed_password="ahshajhdaadasdad", disabled=False),
#             UsersOrm(username="Evilmore",
#                      email="badguy@gmail.com", hashed_password="klxklkplxcmvxm", disabled=False),
#             UsersOrm(username="God",
#                      email="foxpaw@gmail.com", hashed_password="ytreqbbxcm", disabled=False),
#             UsersOrm(username="Zar",
#                      email="petrperv@gmail.com", hashed_password="kiouoimklnlj", disabled=True),
#         ]
#         session.add_all(users)
#         await session.commit()


class Queries:
    @staticmethod
    async def get_user(username: str) -> UserDTO | None:
        async with async_session_factory() as session:
            try:
                query = (
                    select(UsersOrm)
                    .select_from(UsersOrm)
                    .filter_by(username=username)
                )

                response = await session.execute(query)
                user_db = response.scalars().first()
                if not user_db:
                    raise ValueError(f"User <{username}> not found")
            except ValueError as ex:
                # there could be logs
                await session.rollback()

        if user_db:
            user_dto = UserDTO.model_validate(user_db, from_attributes=True)
        else:
            user_dto = None
        return user_dto

    @staticmethod
    async def update_user(user_id: int, new_user_data: UserPostDTO) -> bool:
        async with async_session_factory() as session:
            try:
                if await Queries.__check_duplication_user_data(new_user_data, user_id):
                    user_orm = await session.get(UsersOrm, user_id)
                if not user_orm:
                    raise ValueError(f"User <{user_id}, {new_user_data.username}> doesn't exist")
                for key, item in new_user_data.model_dump().items():
                    setattr(user_orm, key, item)
            except IntegrityError as ex:
                await session.rollback()
                raise ValueError(f"User already exist or incorrect data: {ex.detail}")
            await session.commit()

        # user_send = UserSendDTO.model_validate(new_user_data)
        # user_send.id = user_id
        # await Queries.__synchronize_db(
        #     "update_user",
        #     user_send.model_dump(),
        # )
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

        # await Queries.__synchronize_db("create_user", UserSendDTO.model_validate(user.model_dump()).model_dump())
        return True

    @staticmethod
    async def __check_duplication_user_data(user: UserPostDTO, user_id: int | None = None) -> bool:
        async with async_session_factory() as session:
            try:
                query = (
                    select(
                        UsersOrm.id,
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
                    if user_id:
                        if user_id != record[0] and user.username in record:
                            raise ValueError("Username is already used")
                        elif user_id != record[0] and user.email in record:
                            raise ValueError("Email is already used")
                    else:
                        if user.username in record:
                            raise ValueError("Username is already used")
                        elif user.email in record:
                            raise ValueError("Email is already used")
            except IntegrityError as ex:
                raise ValueError(f"User already exist or incorrect data: {ex.detail}")
        return True

    @staticmethod
    async def delete_user(user_id: int) -> bool:
        async with async_session_factory() as session:
            try:
                user_orm = await session.get(UsersOrm, user_id)
                if not user_orm:
                    raise ValueError(f"User with ID: {user_id} doesn't exist")
                user_orm.disabled = True
            except IntegrityError as ex:
                await session.rollback()
                raise ValueError(f"Something went wrong: {ex.detail}")
            await session.commit()

        # await Queries.__synchronize_db("delete_user", {"id": user_id})
        return True

    @staticmethod
    async def __synchronize_db(topic: str, data: dict):
        pass
        # producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
        # await producer.start()
        # try:
        #     await producer.send_and_wait(topic, json.dumps(data).encode("utf-8"))
        # finally:
        #     await producer.stop()
        # Logger.debug(f"Synchronization:: topic: {topic}, data: {data}")
