from datetime import datetime
from uuid import UUID

from sqlalchemy import asc, desc

from app.database.models.event import Event
from app.database.repositories.events_repository import EventsRepository


class EventsService:
    def __init__(self, events_repository: EventsRepository):
        self.events_repository = events_repository

    async def create_event(self, event_data: dict) -> UUID:
        event_data.update({"tag_id": event_data.pop("tag")})
        event = await self.events_repository.insert_one(event_data)
        return event.id

    async def update_event_by_id(self, new_data: dict, event_id: UUID) -> Event:
        res = await self.events_repository.update_one(new_data, event_id)
        return res

    # status ok or delete result
    async def delete_event(self, event_id: UUID) -> Event:
        return await self.events_repository.delete_one(event_id)

    # what all except get will return dont know
    async def get_events(self, **kwargs):
        data = self.parse_all(**kwargs)
        return await self.events_repository.get_many(
            kwargs.get("limit"),
            kwargs.get("offset"),
            self.parse_sort(kwargs.get("sort")),
            data,
        )

    def parse_sort(self, sort: str):
        sort_params = sort.split(",")
        match sort_params[1]:
            case "desc":
                return desc(sort_params[0])
            case _:
                return asc(sort_params[0])

    def parse_all(self, data: dict):
        parsed_data = {}
        if data.get("locations"):
            parsed_data["location"] = data.get("locations").split(",")
        if data.get("tags"):
            parsed_data["tags"] = data.get("tags").split(",")
        if data.get("organizer"):
            parsed_data["username"] = data.get("organizer")
        if data.get("from_date"):
            parsed_data[""]


# what  return typee
"""
limit:int,offset:int,sort: str | None,locations: str | None,from_date: datetime | None,to_date: datetime | None, tags: str | None,organizer: str | None) -> list[Event]:
        if 
"""
