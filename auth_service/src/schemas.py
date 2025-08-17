from pydantic import BaseModel, EmailStr


class UsersPostDTO(BaseModel):
    username: str
    email: EmailStr


class UsersDTO(UsersPostDTO):
    id: int | None = None
    hashed_password: str
    disabled: bool = False


# class UserSendDTO(BaseModel):
#     id: int
#     disabled: bool


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int
