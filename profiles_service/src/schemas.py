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
    gender: Gender | None = None
    birthday: date | None = None
    zodiac_sign: ZodiacSign | None = None
    description: str | None = None

    @cached_property
    def age(self) -> int | None:
        birthday = self.birthday
        today = date.today()
        age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
        return age


class UsersDTO(UsersPostDTO):
    id: int = Field(frozen=True)
    disabled: bool = False


class ImagesPostDTO(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: int | None
    url: AnyUrl | None


class ImagesDTO(ImagesPostDTO):
    user_id: int


class ShortProfilesDTO(BaseModel):
    user: UsersPostDTO
    profile_picture: ImagesPostDTO | None = None


class ProfilesPostDTO(ShortProfilesDTO):
    images: list[ImagesPostDTO] | None = None


class ProfilesStackDTO(BaseModel):
    profiles: list[ShortProfilesDTO]
