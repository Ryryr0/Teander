from interfaces import IProfilesCacher
from schemas import ProfilesPostDTO


class ProfileCacher(IProfilesCacher):
    async def get_profile_by_user_id(self, user_id: int) -> ProfilesPostDTO:
        ...

    async def cache_profile(self, user_id: int, profile: ProfilesPostDTO) -> bool:
        ...


