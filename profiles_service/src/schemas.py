from typing import Any

from pydantic import BaseModel, EmailStr


class UserPostDTO(BaseModel):
    username: str
    email: EmailStr
    full_name: str


class UserDTO(UserPostDTO):
    id: int
    disabled: bool
