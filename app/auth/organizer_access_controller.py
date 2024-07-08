from typing import Annotated
from uuid import UUID

from fastapi import Path, Depends
from fastapi.security import OAuth2PasswordBearer

from app.auth.auth_service import AuthService
from app.database.repositories.events_repository import EventsRepository
from app.constants.exceptions import Exceptions


class OrganizerAccessController:
    def __init__(self, events_repository: EventsRepository, auth_service: AuthService):
        self.auth_service = auth_service
        self.events_repository = events_repository

    def authorize_creation_role(
        self,
        token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="/api/v1/signin"))],
    ):
        role = self.auth_service.validate_user(token)["role"]
        if role != "ORGANIZER":
            raise Exceptions.ROLE_ERROR.value

    async def verify_organizer_permission(
        self,
        token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="/api/v1/signin"))],
        event_id: UUID = Path(...),
    ):
        user_id = UUID(self.auth_service.validate_user(token)["sub"])
        event = await self.events_repository.get_one(event_id)
        if event.organizer_id != user_id:
            raise Exceptions.PERMISSION_ERROR.value
