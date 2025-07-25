from pydantic import BaseModel, EmailStr


class UserPostDTO(BaseModel):
    username: str
    email: EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int
