import time
from typing import Any
from enum import Enum
from datetime import date
from functools import cached_property

from pydantic import BaseModel, EmailStr, Field, AnyUrl, ConfigDict


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"


class ZodiacSign(str, Enum):
    ARIES = "Aries"
    TAURUS = "Taurus"
    GEMINI = "Gemini"
    CANCER = "Cancer"
    LEO = "Leo"
    VIRGO = "Virgo"
    LIBRA = "Libra"
    SCORPIO = "Scorpio"
    SAGITTARIUS = "Sagittarius"
    CAPRICORN = "Capricorn"
    AQUARIUS = "Aquarius"
    PISCES = "Pisces"


class UsersPostDTO(BaseModel):
    username: str = Field(frozen=True)
    email: EmailStr = Field(frozen=True)
    full_name: str | None = None
    gender: Gender | str | None = None
    birthday: date | None = None
    zodiac_sign: ZodiacSign | str | None = None
    description: str | None = None

    @cached_property
    def age(self) -> int | None:
        today = date.today()
        age = -1
        if self.birthday is not None:
            age = today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
        return age


class UsersDTO(UsersPostDTO):
    id: int = Field(frozen=True)
    disabled: bool = False


class ImagesPostDTO(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: int
    url: AnyUrl


class ImagesDTO(ImagesPostDTO):
    user_id: int


class ShortProfilesDTO(BaseModel):
    id: int
    user: UsersPostDTO
    profile_picture: ImagesPostDTO | None = None


class ProfilesDTO(ShortProfilesDTO):
    images: list[ImagesPostDTO] | None = None


class ProfileStackDTO(BaseModel):
    profiles: list[ShortProfilesDTO]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int
