from uuid import UUID

from sqlalchemy import insert, delete, select

from app.database.db import DB
from app.database.models.registration import Registration


class RegistrationsRepository:
    def __init__(self, db: DB, model: Registration):
        self.db = db
        self.model = model

    async def insert_one(self, data: dict):
        async with self.db.get_sessionmaker() as session:
            stmt = insert(self.model).values(**data)
            res = await session.execute(stmt)
            return res.scalars_one()

    async def delete_one(self, id: UUID):
        async with self.db.get_sessionmaker() as session:
            stmt = delete(self.model).where(self.model.id == id)
            res = await session.execute(stmt)
            return res.scalars_one()

    async def get_one(self, id: UUID):
        async with self.db.get_sessionmaker() as session:
            stmt = select(self.model).where(self.model.id == id)
            res = await session.execute(stmt)
            return res.scalars_one()
