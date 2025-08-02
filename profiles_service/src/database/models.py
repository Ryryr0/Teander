import random
import string
from typing import Callable

from PIL import Image
from sqlalchemy import select, or_, delete
from sqlalchemy.orm import aliased, joinedload
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from interfaces import IUsersDB, IImagesDB, IImagesStorage, IProfilePicturesDB
from schemas import UsersPostDTO, UsersDTO, ImagesPostDTO
from ORM_models import UsersOrm, ImagesOrm, ProfilePicturesOrm
from logger import Logger


class UsersDB(IUsersDB):
    def __init__(self, a_session_factory: Callable[[], AsyncSession]):
        self.a_session_factory = a_session_factory

    async def create_user(self, new_user: UsersPostDTO):
        async with self.a_session_factory() as session:
            try:
                if await self.__check_duplication_user(new_user):
                    session.add(UsersOrm(**new_user.model_dump()))
                else:
                    return False
                await session.commit()
            except IntegrityError as ex:
                await session.rollback()
                Logger.error(f"DataBase IntegrityError: {ex}")
                return False
        return True

    async def get_user_by_id(self, user_id: int) -> UsersDTO | None:
        async with self.a_session_factory() as session:
            try:
                user_orm = await session.get(UsersOrm, user_id)
            except IntegrityError as ex:
                await session.rollback()
                Logger.error(f"DataBase IntegrityError: {ex}")
                return None

        if user_orm:
            user = UsersDTO.model_validate(user_orm, from_attributes=True)
        else:
            user = None
        return user

    async def update_user_by_id(self, user_id: int, new_user_data: UsersDTO) -> bool:
        async with self.a_session_factory() as session:
            try:
                if await self.__check_duplication_user(new_user_data):
                    user_orm = await session.get(UsersOrm, user_id)
                else:
                    return False
                if user_orm:
                    for attr, value in new_user_data.model_dump().items():
                        if attr not in ["id", "username", "email", "disabled"]:
                            setattr(user_orm, attr, value)
                else:
                    return False
                await session.commit()
            except IntegrityError as ex:
                await session.rollback()
                Logger.error(f"DataBase IntegrityError: {ex}")
                return False
        return True

    async def delete_user_by_id(self, user_id: int) -> bool:
        async with self.a_session_factory() as session:
            try:
                user = await session.get(UsersOrm, user_id)
                user.disabled = True
                await session.commit()
            except IntegrityError as ex:
                await session.rollback()
                Logger.error(f"DataBase IntegrityError: {ex}")
                return False
        return True

    async def __check_duplication_user(self, user: UsersPostDTO) -> bool:
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

        async with self.a_session_factory() as session:
            try:
                exec_result = await session.execute(query)
                results = exec_result.all()
                if not results:
                    return False
            except IntegrityError as ex:
                await session.rollback()
                Logger.error(f"DataBase IntegrityError: {ex}")
                return False
        return True


# Temporary solution
class ImagesStorage(IImagesStorage):
    async def save_image(self, image: Image.Image) -> str:
        return random.choices(string.ascii_letters + string.digits, k=20)

    async def delete_image(self, image_id: int) -> bool:
        return True


class ImagesDB(IImagesDB):
    def __init__(self, a_session_factory: Callable[[], AsyncSession], images_storage: IImagesStorage):
        self.a_session_factory = a_session_factory
        self.images_storage = images_storage

    async def get_images_by_user_id(self, user_id: int) -> list[ImagesPostDTO]:
        query = (
            select(
                ImagesOrm.id.label("id"),
                ImagesOrm.url.label("url"),
            ).select_from(ImagesOrm)
            .filter(ImagesOrm.user_id == user_id)
        )
        images_list = []

        async with self.a_session_factory() as session:
            try:
                exec_result = await session.execute(query)
                results = exec_result.fetchall()
                if results:
                    for record in results:
                        images_list.append(ImagesPostDTO(id=record.id, url=record.url))
            except IntegrityError as ex:
                await session.rollback()
                Logger.error(f"DataBase IntegrityError: {ex}")
                return images_list
        return images_list

    async def save_image(self, image: Image.Image, user_id: int) -> bool:
        if not (url := self.images_storage.save_image(image)):
            return False

        async with self.a_session_factory() as session:
            try:
                session.add(ImagesOrm(url=url, user_id=user_id))
                await session.commit()
            except IntegrityError as ex:
                await session.rollback()
                Logger.error(f"DataBase IntegrityError: {ex}")
                return False
        return True

    async def delete_image(self, image_id: int) -> bool:
        query = (
            delete(ImagesOrm)
            .where(ImagesOrm.id == image_id)
        )

        async with self.a_session_factory() as session:
            try:
                await session.execute(query)
                if not self.images_storage.delete_image(image_id):
                    await session.rollback()
                    return False
                await session.commit()
            except IntegrityError as ex:
                await session.rollback()
                Logger.error(f"DataBase IntegrityError: {ex}")
                return False
        return True


class ProfilePicturesDB(IProfilePicturesDB):
    def __init__(self, a_session_factory: Callable[[], AsyncSession], images_storage: IImagesStorage):
        self.a_session_factory = a_session_factory
        self.images_storage = images_storage

    async def get_profile_picture_by_user_id(self, user_id: int) -> ImagesPostDTO | None:
        query = (
            select(ProfilePicturesOrm)
            .filter(ProfilePicturesOrm.user_id == user_id)
            .options(joinedload(ProfilePicturesOrm.image))
        )

        async with self.a_session_factory() as session:
            try:
                exec_result = await session.execute(query)
                result = exec_result.scalars().first()
                if not result:
                    return None
            except IntegrityError as ex:
                await session.rollback()
                Logger.error(f"DataBase IntegrityError: {ex}")
                return None
        return ImagesPostDTO(id=result.image.id, url=result.image.url)

    async def save_profile_picture(self, image: Image.Image, user_id: int) -> bool:
        if not (url := self.images_storage.save_image(image)):
            return False

        async with self.a_session_factory() as session:
            try:
                image_orm = ImagesOrm(url=url, user_id=user_id)
                session.add(image_orm)
                await session.flush()
                session.add(ProfilePicturesOrm(user_id=user_id, image_id=image_orm.id))
                await session.commit()
            except IntegrityError as ex:
                await session.rollback()
                Logger.error(f"DataBase IntegrityError: {ex}")
                return False
        return True

    async def set_profile_picture(self, image_id: int, user_id: int) -> bool:
        query = (
            select(UsersOrm)
            .select_from(UsersOrm)
            .filter(UsersOrm.id == user_id)
            .options(joinedload(UsersOrm.profile_picture))
        )

        async with self.a_session_factory() as session:
            try:
                ...
            except IntegrityError as ex:
                await session.rollback()
                Logger.error(f"DataBase IntegrityError: {ex}")
                return False
        return True
