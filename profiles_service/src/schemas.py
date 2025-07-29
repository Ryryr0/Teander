from typing import Any
from enum import Enum
from datetime import date

from pydantic import BaseModel, EmailStr, field_validator, Field, AnyUrl, ConfigDict


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
    full_name: str
    gender: Gender
    birthday: date
    age: int | None
    zodiac_sign: ZodiacSign | None
    description: str | None

    @field_validator("age", mode="plain")
    @classmethod
    def count_age(cls, value: Any) -> int:
        birthday = cls.birthday
        if not birthday:
            raise ValueError("birthday is required to calculate age")
        today = date.today()
        age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
        return age


class UsersDTO(UsersPostDTO):
    id: int = Field(frozen=True)
    disabled: bool


class ImagesPostDTO(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: int
    url: AnyUrl


class ImagesDTO(ImagesPostDTO):
    user_id: int


class ShortProfilesDTO(BaseModel):
    user: UsersPostDTO
    profile_picture: ImagesPostDTO


class FullProfilesDTO(ShortProfilesDTO):
    user_images: list[ImagesPostDTO]


class ProfilesStackDTO(BaseModel):
    profiles: list[ShortProfilesDTO]
