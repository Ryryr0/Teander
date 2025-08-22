from redis.asyncio import Redis

from config import settings
from interfaces import IProfilesCacher, ICacheCleaner
from schemas import ProfilesDTO
from logger import Logger


class CacheCleaner(ICacheCleaner):
    def __init__(self):
        self._redis = Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=0
        )

    async def delete_cache(self, user_id) -> bool:
        async with self._redis.pipeline(transaction=True) as pipe:
            await pipe.delete(f"profile:{user_id}")
            result: bool = bool(await pipe.execute())
        if result:
            Logger.info(f"Cache user<id: {user_id}> cleaned")
        else:
            Logger.warning(f"Cache user<id: {user_id}> not cleaned")
        return result


class ProfileCacher(CacheCleaner, IProfilesCacher):
    def __init__(self):
        super().__init__()

    async def get_profile_by_user_id(self, user_id: int) -> ProfilesDTO | None:
        async with self._redis.pipeline(transaction=True) as pipe:
            await pipe.get(f"profile:{user_id}") 
            result = await pipe.execute()
        if result[0] is None:
            return None
        result = result[0].decode()
        profile_post = ProfilesDTO.model_validate_json(result)
        if profile_post:
            Logger.info(f"Cached user<id: {user_id}> received")
        else:
            Logger.info(f"Cached user<id: {user_id}> not received")
        return profile_post

    async def cache_profile(self, user_id: int, profile: ProfilesDTO) -> bool:
        async with self._redis.pipeline(transaction=True) as pipe:
            await pipe.setex(f"profile:{user_id}", 60, profile.model_dump_json())
            result: bool = bool(await pipe.execute())
        if result:
            Logger.info(f"Cache user<id: {user_id}> cached")
        else:
            Logger.warning(f"Cache user<id: {user_id}> not cached")
        return result
