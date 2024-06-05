from uuid import UUID

from sqlalchemy import insert, select

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

    async def get_one(self, id: UUID):
        async with self.db.get_sessionmaker() as session:
            stmt = select(self.model).where(self.model.id == id)
            res = await session.execute(stmt)
            return res
