from uuid import UUID

from app.auth.auth_service import AuthService
from app.core.users_service import UsersService
from app.schemas.registration_schema import RegistrationDto
from app.core.registrations_service import RegistrationsService
from app.notifications.email_service import EmailService
from fastapi import APIRouter, Depends


class RegistrationsRouter:
    def __init__(
        self,
        email_service: EmailService,
        registration_service: RegistrationsService,
        users_service: UsersService,
        auth_service: AuthService,
    ):
        self.email_service = email_service
        self.auth_service = auth_service
        self.registration_service = registration_service
        self.users_service = users_service
        self.router = APIRouter(
            prefix="/api/v1/registrations",
            tags=["event_registration"],
            dependencies=[Depends(self.auth_service.validate_user)],
        )

    def get_router(self) -> APIRouter:
        self.router.post("/")(self.create_registration)
        self.router.delete("/{registration_id}")(self.cancel_event)
        return self.router

    async def create_registration(self, registration: RegistrationDto) -> dict:
        res = await self.registration_service.create_registration(
            registration.model_dump()
        )
        self.email_service.send_email(
            await self.users_service.get_email(registration.user_id),
            content="event_registration",
        )
        return {"registration_id": res}

    async def cancel_event(self, registration_id: UUID):
        res = await self.registration_service.delete_registration(registration_id)
        self.email_service.send_email(
            await self.users_service.get_email(res.user_id),
            content="event_cancellation",
        )
        return res
