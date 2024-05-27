from uuid import UUID

from app.database.models.event import Event
from app.database.repositories.events_repository import EventsRepository


class EventsService:
    def __init__(self, events_repository: EventsRepository):
        self.events_repository = events_repository

    async def create_event(self, event_data: dict) -> UUID:
        event_data.update({"tag_id": event_data.pop("tag")})
        event = await self.events_repository.create_event(event_data)
        return event.id

    async def update_event_by_id(self, description: str, event_id: UUID) -> Event:
        res = await self.events_repository.update_event(
            {"description": description}, event_id
        )
        return res
