from typing import Any
import io
import datetime

import pytest
from PIL import Image

from src.controllers import *
from fastapi import UploadFile
from fake_db_models import FakeUsersDB, FakeImagesDB, FakeProfilesCacher, FakeProfilePicturesDB
from src.schemas import ZodiacSign, Gender, UsersPostDTO, UsersDTO, ImagesPostDTO, ProfilesPostDTO, ShortProfilesDTO


full_user_data = {
    "username": "test_user1",
    "email": "testuser1@fake.ru",
    "full_name": "Test User",
    "gender": Gender.MALE,
    "birthday": datetime.date(year=2004, month=2, day=8),
    "zodiac_sign": ZodiacSign.AQUARIUS,
    "description": "Test description",
}

min_user_data: dict[str, Any] = {
    "username": "test_user2",
    "email": "testuser2@fake.ru",
}

new_min_user_data = {
    "username": "test_user2",
    "email": "testuser2@fake.ru",
    "full_name": "Mini Test User",
    "gender": Gender.FEMALE,
    "birthday": datetime.date(year=1999, month=1, day=10),
    "zodiac_sign": ZodiacSign.SCORPIO,
    "description": "Mini test description",
}

wrong_min_user_data: dict[str, Any] = {
    "username": "wrong_test_user2",
    "email": "wrong_testuser2@fake.ru",
}


@pytest.fixture(scope="function")
def create_all_controllers():
    controllers = {}
    controllers.update(
        users=Users(FakeUsersDB()),
        images=Images(FakeImagesDB()),
        profile_pictures=ProfilePictures(FakeProfilePicturesDB(FakeImagesDB())),
        profile_cacher=FakeProfilesCacher(),
    )
    return controllers


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


async def test_users_p():
    users = Users(FakeUsersDB())
    full_user = UsersDTO(id=1, **full_user_data)
    full_user_post = UsersPostDTO(**full_user_data)
    min_user = UsersDTO(id=2, **min_user_data)
    min_user_post = UsersPostDTO(**min_user_data)
    new_min_user = UsersDTO(id=2, **new_min_user_data)
    new_min_user_post = UsersPostDTO(**new_min_user_data)

    assert await users.create_user(1, full_user_post) is True
    assert await users.create_user(2, min_user_post) is True
    assert await users.get_user(1) == full_user
    assert await users.get_user(2) == min_user
    assert await users.update_user(2, new_min_user_post) is True
    assert await users.get_user(2) == new_min_user
    assert await users.delete_user(1) is True
    assert await users.get_user(1) is None


async def test_users_n():
    users = Users(FakeUsersDB())
    min_user = UsersDTO(id=1, **min_user_data)
    min_user_post = UsersPostDTO(**min_user_data)
    wrong_min_user_post = UsersPostDTO(**wrong_min_user_data)

    assert await users.create_user(1, min_user_post) is True
    assert await users.create_user(1, min_user_post) is False
    assert await users.create_user(2, min_user_post) is False
    assert await users.update_user(1, wrong_min_user_post) is True
    assert await users.get_user(1) == min_user
    assert await users.delete_user(2) is False
    assert await users.get_user(2) is None


async def test_images(create_image):
    images = Images(FakeImagesDB())
    fake_image = UploadFile(filename="tets.png", file=create_image)

    assert await images.save_user_image(fake_image,  1) is True
    assert await images.get_user_images(1) != []
    assert await images.delete_user_images(1) is True


async def test_profile_pictures(create_image):
    profile_pictures = ProfilePictures(FakeProfilePicturesDB(FakeImagesDB()))
    fake_image = UploadFile(filename="tets.png", file=create_image)

    assert await profile_pictures.create_profile_pictures(1)
    assert await profile_pictures.save_user_profile_picture(fake_image, 1) is True
    assert await profile_pictures.get_user_profile_picture(1) is not None
    assert await profile_pictures.set_user_profile_picture(1, 1) is True
    assert await profile_pictures.delete_user_profile_picture(1) is True


async def test_profiles(create_all_controllers, create_image):
        profiles = Profiles(**create_all_controllers)
        user_post = UsersPostDTO(**full_user_data)

        assert await profiles.create_profile(1, user_post)
        assert await profiles.get_profile(1) is not None
        assert await profiles.get_profile(1) is not None
        assert await profiles.get_short_profile(1) is not None
        assert await profiles.get_short_profile(1) is not None
        assert await profiles.update_profile(1, user_post)
        assert await profiles.delete_profile(1)
