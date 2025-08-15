import asyncio
import time

from redis.asyncio import Redis

from config import settings
from interfaces import IProfilesCacher
from schemas import ProfilesPostDTO


class ProfileCacher(IProfilesCacher):
    def __init__(self):
        self.__redis = Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=0
        )

    async def get_profile_by_user_id(self, user_id: int) -> ProfilesPostDTO | None:
        async with self.__redis.pipeline(transaction=True) as pipe:
            await pipe.get(f"profile:{user_id}") 
            result = await pipe.execute()
        if result[0] is None:
            return None
        result = result[0].decode()
        profile_post = ProfilesPostDTO.model_validate_json(result)
        await self.cache_profile(user_id, profile_post)
        return profile_post

    async def cache_profile(self, user_id: int, profile: ProfilesPostDTO) -> bool:
        async with self.__redis.pipeline(transaction=True) as pipe:
            await pipe.setex(f"profile:{user_id}", 60, profile.model_dump_json())
            result: bool = bool(await pipe.execute())
        return result

    async def delete_cache(self, user_id) -> bool:
        async with self.__redis.pipeline(transaction=True) as pipe:
            await pipe.delete(f"profile:{user_id}")
            result: bool = bool(await pipe.execute())
        return result
