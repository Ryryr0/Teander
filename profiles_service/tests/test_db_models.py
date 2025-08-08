import datetime
import pytest
import io

from PIL import Image
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from database.models import UsersDB, ImagesDB, ImagesStorage, ProfilePicturesDB
from database.ORM_models import Base
from schemas import UsersPostDTO, ZodiacSign, Gender, UsersDTO, ImagesPostDTO
from config import settings

full_user_data = {
    "username": "test_user1",
    "email": "testuser1@fake.ru",
    "full_name": "Test User",
    "gender": Gender.MALE,
    "birthday": "2004-02-08",
    "zodiac_sign": ZodiacSign.AQUARIUS,
    "description": "Test description",
}

min_user_data = {
    "username": "test_user2",
    "email": "testuser2@fake.ru",
}

new_min_user_data = {
    "username": "test_user2",
    "email": "testuser2@fake.ru",
    "full_name": "Mini Test User",
    "gender": Gender.FEMALE,
    "birthday": "1999-01-10",
    "zodiac_sign": ZodiacSign.SCORPIO,
    "description": "Mini test description",
}

wrong_min_user_data = {
    "username": "wrong_test_user2",
    "email": "wrong_testuser2@fake.ru",
}


@pytest.fixture(scope="function")
async def create_engine():
    async_engine = create_async_engine(
        url=settings.DATABASE_URL,
        echo=False,
    )
    return async_engine


@pytest.fixture(scope="function")
async def setup_db(create_engine):
    async with create_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield async_sessionmaker(create_engine)

    async with create_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def create_image():
    image_format = "PNG"
    size = (100, 100)
    color = (255, 0, 0)
    image = Image.new("RGB", size, color)
    byte_io = io.BytesIO()
    image.save(byte_io, format=image_format)
    byte_io.seek(0)
    return byte_io


async def test_user_db_p(setup_db):
    user_db = UsersDB(a_session_factory=setup_db)
    full_user_post = UsersPostDTO(**full_user_data)
    min_user_post = UsersPostDTO(**min_user_data)
    new_min_user_post = UsersPostDTO(**new_min_user_data)
    new_min_user = UsersDTO(**new_min_user_data, id=2)
    full_user = UsersDTO(**full_user_data, id=1)
    min_user = UsersDTO(**min_user_data, id=2)

    # Testing creation
    assert await user_db.create_user(1, full_user_post) is True
    assert await user_db.create_user(2, min_user_post) is True
    # Testing getting
    assert await user_db.get_user_by_id(1) == full_user
    assert await user_db.get_user_by_id(2) == min_user
    # Testing updating
    assert await user_db.update_user_by_id(2, new_min_user_post) is True
    assert await user_db.get_user_by_id(2) == new_min_user
    # Testing deleting
    assert await user_db.delete_user_by_id(1) is True
    assert await user_db.get_user_by_id(1) is None


async def test_users_db_n(setup_db):
    user_db = UsersDB(a_session_factory=setup_db)
    min_user_post = UsersPostDTO(**min_user_data)
    wrong_user_post = UsersPostDTO(**wrong_min_user_data)
    min_user = UsersDTO(**min_user_data, id=1)

    assert await user_db.create_user(1, min_user_post) is True
    assert await user_db.create_user(1, min_user_post) is False
    assert await user_db.update_user_by_id(1, wrong_user_post) is True
    assert await user_db.get_user_by_id(1) == min_user


async def test_images_db_p(setup_db, create_image):
    # Filling db with users
    user_db = UsersDB(a_session_factory=setup_db)
    full_user_post = UsersPostDTO(**full_user_data)
    await user_db.create_user(1, full_user_post)  # id = 1

    images_storage = ImagesStorage()
    images_db = ImagesDB(setup_db, images_storage)
    fake_image = Image.open(create_image)

    assert await images_db.save_image(fake_image, 1) is True
    image_list = await images_db.get_images_by_user_id(1)
    assert len(image_list) == 1
    assert isinstance(image_list[0], ImagesPostDTO) is True
    assert image_list[0].id == 1
    assert await images_db.delete_image(1) is True
    image_list = await images_db.get_images_by_user_id(1)
    assert len(image_list) == 0


async def test_images_db_n(setup_db, create_image):
    images_storage = ImagesStorage()
    images_db = ImagesDB(setup_db, images_storage)
    fake_image = Image.open(create_image)

    assert await images_db.save_image(fake_image, 2) is False
    assert await images_db.get_images_by_user_id(2) == []
    # assert await images_db.delete_image(1) is False


async def test_profile_pictures_db_p(setup_db, create_image):
    # Filling db with users and image
    user_db = UsersDB(a_session_factory=setup_db)
    full_user_post = UsersPostDTO(**full_user_data)
    await user_db.create_user(1, full_user_post)  # id = 1
    images_storage = ImagesStorage()
    images_db = ImagesDB(setup_db, images_storage)
    fake_image = Image.open(create_image)
    await images_db.save_image(fake_image, 1)  # id = 1

    profile_pictures_db = ProfilePicturesDB(setup_db, images_storage)

    assert await profile_pictures_db.set_profile_picture(1, 1) is True
    gotten_image = await profile_pictures_db.get_profile_picture_by_user_id(1)
    assert isinstance(gotten_image, ImagesPostDTO) is True
    assert gotten_image.id == 1
    await images_db.delete_image(1)
    gotten_image = await profile_pictures_db.get_profile_picture_by_user_id(1)
    assert gotten_image is None
    assert await profile_pictures_db.save_profile_picture(fake_image, 1) is True
    gotten_image = await profile_pictures_db.get_profile_picture_by_user_id(1)
    assert isinstance(gotten_image, ImagesPostDTO) is True
    assert gotten_image.id == 2
    assert await profile_pictures_db.delete_profile_picture(1)
    assert await profile_pictures_db.get_profile_picture_by_user_id(1) is None


async def test_profile_pictures_db_n(setup_db, create_image):
    # Filling db with users and image
    user_db = UsersDB(a_session_factory=setup_db)
    full_user_post = UsersPostDTO(**full_user_data)
    await user_db.create_user(1, full_user_post)  # id = 1
    images_storage = ImagesStorage()
    images_db = ImagesDB(setup_db, images_storage)
    fake_image = Image.open(create_image)
    await images_db.save_image(fake_image, 1)  # id = 1

    profile_pictures_db = ProfilePicturesDB(setup_db, images_storage)

    assert await profile_pictures_db.get_profile_picture_by_user_id(1) is None
    assert await profile_pictures_db.set_profile_picture(2, 1) is False
    assert await profile_pictures_db.set_profile_picture(1, 2) is False
