from uuid import UUID

from sqlalchemy import insert, select, update

from app.database.db import DB
from app.database.models.user import User


class UsersRepository:
    def __init__(self, db: DB):
        self.db = db
        self.model = User

    async def insert_one(self, user_data: dict) -> UUID:
        async with self.db.get_sessionmaker() as session:
            stmt = insert(self.model).values(**user_data).returning(self.model.id)
            res = await session.execute(stmt)
            return res.scalar_one()

    async def get_one(self, id: UUID) -> User:
        async with self.db.get_sessionmaker() as session:
            stmt = select(self.model).where(self.model.id == id)
            res = await session.execute(stmt)
            return res.scalar_one()

    async def get_one_by_username(self, username: str) -> User:
        async with self.db.get_sessionmaker() as session:
            stmt = select(self.model).where(self.model.username == username)
            res = await session.execute(stmt)
            return res.scalar_one()

    async def update_one(self, new_data: dict, id: UUID) -> UUID:
        async with self.db.get_sessionmaker() as session:
            stmt = (
                update(self.model)
                .values(**new_data)
                .where(self.model.id == id)
                .returning(self.model.id)
            )
            res = await session.execute(stmt)
            return res.scalar_one()

    async def get_one_by_token(self, token: UUID) -> User:
        async with self.db.get_sessionmaker() as session:
            stmt = select(self.model).where(self.model.refresh_token == token)
            res = await session.execute(stmt)
            return res.scalar_one()
