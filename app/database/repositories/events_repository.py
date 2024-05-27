from uuid import UUID

from sqlalchemy import insert, update

from app.database.db import DB
from app.database.models.event import Event


class EventsRepository:
    def __init__(self, db: DB, model: Event):
        self.db = db
        self.model = model

    async def create_event(self, event_data: dict):
        async with self.db.get_sessionmaker() as session:
            stmt = insert(self.model).values(**event_data)
            res = await session.execute(stmt)
            return res.scalars_one()

    async def update_event(self, new_data: dict, event_id: UUID):
        async with self.db.get_sessionmaker() as session:
            stmt = (
                update(self.model).values(**new_data).where(self.model.id == event_id)
            )
            res = await session.execute(stmt)
            return res.scalars_one()
