from sqlalchemy import insert

from app.database.db import DB
from app.database.models.user import User


class UsersRepository:
    def __init__(self, db: DB, model: User):
        self.db = db
        self.model = model

    async def insert_one(self, user_data: dict):
        async with self.db.get_sessionmaker() as session:
            stmt = insert(self.model).values(**user_data)
            res = await session.execute(stmt)
            return res.scalars_one()
