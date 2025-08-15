import time

from src.database.cachers import ProfileCacher
from src.schemas import ProfilesPostDTO, UsersPostDTO


async def test_cacher():
    pc = ProfileCacher()
    profile = ProfilesPostDTO(user=UsersPostDTO(username="user1", email="user1@gmail.com"))

    assert await pc.cache_profile(1, profile)
    assert await pc.get_profile_by_user_id(1) == profile
    time.sleep(61)
    assert await pc.get_profile_by_user_id(1) is None
    assert await pc.cache_profile(1, profile)
    time.sleep(5)
    assert await pc.cache_profile(1, profile)
    time.sleep(56)
    assert await pc.get_profile_by_user_id(1) == profile
    assert await pc.cache_profile(1, profile)
    assert await pc.delete_cache(1)
    assert await pc.get_profile_by_user_id(1) is None
