from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.orm import Mapped, mapped_column

from database import DataBase


class UsersOrm(DataBase):
    __table_name__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    full_name: Mapped[str]
    email: Mapped[str] = mapped_column(email=True)
    hashed_password: Mapped[str]
    disabled: Mapped[bool]

