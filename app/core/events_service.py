from uuid import UUID

from sqlalchemy import asc, desc, JSON

from app.database.models.event import Event
from app.database.repositories.events_repository import EventsRepository
from app.utils.query_builder import QueryBuilder


class EventsService:
    def __init__(self, events_repository: EventsRepository,query_builder: QueryBuilder):
        self.events_repository = events_repository
        self.query_builder = query_builder

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

    async def get_events(self, **kwargs):
        return await self.events_repository.get_many(
            kwargs.get("limit"),
            kwargs.get("offset"),
            self.parse_sort(kwargs.get("sort"))
        )

    def parse_sort(self, sort: str):
        sort_params = sort.split(",")
        match sort_params[1]:
            case "desc":
                return desc(sort_params[0])
            case _:
                return asc(sort_params[0])

    async def get_filtered_events(self,data: dict):
        return  await self.events_repository.get_all_by_filters(self.query_builder.execute_query(data))




