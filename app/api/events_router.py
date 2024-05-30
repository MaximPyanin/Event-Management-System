import datetime
from uuid import UUID

from fastapi import APIRouter

from app.constants.tags import Tags
from app.database.models.event import Event
from app.schemas.event_schema import EventCreationDto
from app.core.events_service import EventsService
from app.schemas.event_schema import EventUpdateDto

class EventsRouter:
    def __init__(self,events_service: EventsService):
        self.events_service = events_service
        self.router = APIRouter(
            prefix="/api/v1/events",tags=["Events"]
        )

    def get_router(self) -> APIRouter:
        self.router.post("/")(self.create_event)
        self.router.patch("/{event_id}")(self.update_event)
        self.router.delete("/{event_id}")(self.delete_event)
        self.router.get("/")(self.get_events)
        return self.router
    #advanced search , how to call path inside routers of features for post here events/?
    async def create_event(self,event_data: EventCreationDto) -> dict:
        event_id = await self.events_service.create_event(event_data.model_dump())
        return {"event_id":event_id}#as key event id or just id
#for dele te update whsat pathh
#return event
    async def update_event(self,event_id: UUID,data: EventUpdateDto ) -> Event:
        return await self.events_service.update_event_by_id(data.model_dump(),event_id)

    async def delete_event(self, event_id: UUID):
        return await self.events_service.delete_event(event_id)

    async def get_events(self,locations: str= None,from_date: datetime.datetime = None ,to_date: datetime.datetime = None, tags: str  = None,sort: str = None, organizer: str =None,limit:int = 10,offset: int = 0) -> list[Event]:
        return await self.events_service.get_events(limit=limit,locations=locations,offset=offset,sort=sort,from_date=from_date,to_date=to_date,tags=tags,organizer=organizer)
