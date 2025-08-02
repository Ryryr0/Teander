from typing import Annotated
from datetime import date

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from schemas import Gender, ZodiacSign


intpk = Annotated[int, mapped_column(primary_key=True)]
str_256 = Annotated[str, 256]


class Base(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256)
    }

    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__}: {', '.join(cols)}>"


class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    username: Mapped[str_256] = mapped_column(unique=True)
    email: Mapped[str_256] = mapped_column(unique=True)
    full_name: Mapped[str_256]
    gender: Mapped[Gender]
    birthday: Mapped[date | None]
    zodiac_sign: Mapped[ZodiacSign | None]
    description: Mapped[str | None]
    disabled: Mapped[bool] = mapped_column(default=False)

    profile_picture: Mapped["ProfilePicturesOrm"] = relationship(back_populates="user")


class ImagesOrm(Base):
    __tablename__ = "images"

    id: Mapped[intpk]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    url: Mapped[str]

    profile_picture: Mapped["ProfilePicturesOrm"] = relationship(back_populates="image")


class ProfilePicturesOrm(Base):
    __tablename__ = "profile_pictures"

    image_id: Mapped[int] = mapped_column(ForeignKey("images.id", ondelete="SET NULL"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    image: Mapped["ImagesOrm"] = relationship(back_populates="profile_picture")
    user: Mapped["UsersOrm"] = relationship(back_populates="profile_picture")
