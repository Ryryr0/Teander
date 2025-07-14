from pydantic import BaseModel


class UserPostDTO(BaseModel):
    username: str
    email: str


class UserDTO(UserPostDTO):
    id: int | None = None
    hashed_password: str
    disabled: bool = False


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int
