from typing import Sequence, Any
from uuid import UUID

from fastapi import APIRouter, Depends, Body


from app.auth.auth_service import AuthService
from app.auth.organizer_access_controller import OrganizerAccessController
from app.database.models.event import Event
from app.schemas.event_schema import EventCreationDto
from app.core.events_service import EventsService
from app.schemas.event_schema import EventUpdateDto

from sqlalchemy import Row, RowMapping


class EventsRouter:
    def __init__(
        self,
        events_service: EventsService,
        auth_service: AuthService,
        organizer_access_controller: OrganizerAccessController,
    ):
        self.events_service = events_service
        self.auth_service = auth_service
        self.organizer_access_controller = organizer_access_controller
        self.router = APIRouter(prefix="/api/v1/events", tags=["Events"])

    def get_router(self) -> APIRouter:
        self.router.post(
            "/",
            dependencies=[
                Depends(self.auth_service.validate_user),
                Depends(self.organizer_access_controller.authorize_creation_role),
            ],
        )(self.create_event)
        self.router.put(
            "/{event_id}",
            response_model=None,
            dependencies=[
                Depends(self.auth_service.validate_user),
                Depends(self.organizer_access_controller.verify_organizer_permission),
            ],
        )(self.update_event)
        self.router.delete(
            "/{event_id}",
            response_model=None,
            dependencies=[
                Depends(self.auth_service.validate_user),
                Depends(self.organizer_access_controller.verify_organizer_permission),
            ],
        )(self.delete_event)
        self.router.get("/", response_model=None)(self.get_events)
        self.router.post("/filter", response_model=None)(self.filter)
        return self.router

    async def create_event(self, event_data: EventCreationDto) -> dict:
        event_id = await self.events_service.create_event(event_data.model_dump())
        return {"event_id": event_id}

    async def update_event(self, event_id: UUID, data: EventUpdateDto) -> Event:
        return await self.events_service.update_event_by_id(data.model_dump(), event_id)

    async def delete_event(self, event_id: UUID) -> Event:
        return await self.events_service.delete_event(event_id)

    async def get_events(
        self,
        sort: str = None,
        limit: int = 10,
        offset: int = 0,
    ) -> Sequence[Event]:
        print(limit, offset)
        return await self.events_service.get_events(
            limit=limit, offset=offset, sort=sort
        )

    async def filter(
        self, to_filter: dict = Body(...)
    ) -> Sequence[Row | RowMapping | Any]:
        return await self.events_service.get_filtered_events(to_filter)
