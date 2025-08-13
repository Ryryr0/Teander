from fastapi.routing import APIRouter

from schemas import ProfileStackDTO
from dependencies import UserId


router = APIRouter(
    prefix="/stacks",
    tags=["stacks"],
    responses={404: {"description": "User profile not found"}},
)


@router.get(path="", response_model=ProfileStackDTO)
async def get_profile_stack(user_id: UserId):
    ...
