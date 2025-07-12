from sqlalchemy import text, insert

from database import DataBase
from models import UsersOrm


async def insert_data():
    async with DataBase.get_session() as session:
        user_bobr = UsersOrm()
