import datetime
from uuid import UUID

from sqlalchemy import insert, update, delete, select, UnaryExpression
from sqlalchemy.orm import selectinload, joinedload

from app.database.db import DB
from app.database.models.event import Event


class EventsRepository:
    def __init__(self, db: DB, model: Event):
        self.db = db
        self.model = model

    async def insert_one(self, event_data: dict):
        async with self.db.get_sessionmaker() as session:
            stmt = insert(self.model).values(**event_data)
            res = await session.execute(stmt)
            return res.scalars_one()

    async def update_one(self, new_data: dict, event_id: UUID):
        async with self.db.get_sessionmaker() as session:
            stmt = (
                update(self.model).values(**new_data).where(self.model.id == event_id)
            )
            res = await session.execute(stmt)
            return res.scalars_one()

    async def delete_one(self, event_id: UUID):
        async with self.db.get_sessionmaker() as session:
            stmt = delete(self.model).where(self.model.id == event_id)
            res = await session.execute(stmt)
            return res.scalars_one()

    async def get_many(
        self, limit: int, offset: int, sort: UnaryExpression | None
    ):
        async with self.db.get_sessionmaker() as session:
            stmt = (
                select(self.model)
                .options(selectinload(self.model.tag))
                .options(selectinload(self.model.organizer))
                .options(joinedload(self.model.feedbacks))
                .order_by(sort)
                .offset(offset)
                .limit(limit)
            )
            res = await session.execute(stmt)
            return res.unique().scalars().all()

    async def get_all(self, date: datetime.date) -> list[Event]:
        async with self.db.get_sessionmaker() as session:
            stmt = (
                select(self.model)
                .options(selectinload(self.model.users))
                .where(self.model.date == date)
            )
            res = await session.execute(stmt)
            return res.scalars().all()

    async def get_all_by_filters(self,query: select):
        async with self.db.get_sessionmaker() as session:
            res = await session.execute(query)
            return res.unique().scalars().all()


