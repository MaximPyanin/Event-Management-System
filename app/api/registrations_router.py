from uuid import UUID

from app.schemas.registration_schema import RegistrationDto
from app.core.registrations_service import RegistrationsService
from app.notifications.email_service import EmailService
from fastapi import APIRouter


class RegistrationsRouter:
    def __init__(self, email_service: EmailService,registration_service: RegistrationsService):
        self.email_service = email_service
        self.registration_service = registration_service
        self.router = APIRouter(prefix="/api/v1/registrations", tags=["event_registration"])

    def get_router(self) -> APIRouter:
        self.router.post("/")(self.create_registration)
        self.router.delete("/{registration_id}")(self.cancel_event)
        return self.router
    async def create_registration(self,registration: RegistrationDto):
        res = await self.registration_service.create_registration(registration.model_dump())
        await self.email_service.send_email()
        return res

    async def cancel_event(self,registration_id: UUID):
        return await self.registration_service.delete_registration(registration_id)

