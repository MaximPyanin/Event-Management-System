import datetime
from uuid import UUID

from sqlalchemy import insert, update, delete, select, UnaryExpression
from sqlalchemy.orm import selectinload, joinedload

from app.database.db import DB
from app.database.models.event import Event


class EventsRepository:
    def __init__(self, db: DB):
        self.db = db
        self.model = Event

    async def insert_one(self, event_data: dict) -> UUID:
        async with self.db.get_sessionmaker() as session:
            stmt = insert(self.model).values(**event_data).returning(self.model.id)
            res = await session.execute(stmt)
            return res.scalars_one()

    async def update_one(self, new_data: dict, event_id: UUID) -> Event:
        async with self.db.get_sessionmaker() as session:
            stmt = (
                update(self.model)
                .values(**new_data)
                .where(self.model.id == event_id)
                .returning(self.model)
            )
            res = await session.execute(stmt)
            return res.scalars_one()

    async def delete_one(self, event_id: UUID) -> Event:
        async with self.db.get_sessionmaker() as session:
            stmt = (
                delete(self.model)
                .where(self.model.id == event_id)
                .returning(self.model)
            )
            res = await session.execute(stmt)
            return res.scalars_one()

    async def get_many(
        self, limit: int, offset: int, sort: UnaryExpression | None
    ) -> list[Event]:
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

    async def get_all_by_filters(self, query: select) -> list[Event]:
        async with self.db.get_sessionmaker() as session:
            res = await session.execute(query)
            return res.unique().scalars().all()

    async def get_one(self, id: UUID) -> Event:
        async with self.db.get_sessionmaker() as session:
            stmt = select(self.model).where(self.model.id == id)
            res = await session.execute(stmt)
            return res.scalars_one()
