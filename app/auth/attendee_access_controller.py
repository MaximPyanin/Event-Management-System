from typing import Annotated
from uuid import UUID

from fastapi import Path, Depends
from fastapi.security import OAuth2PasswordBearer

from app.auth.auth_service import AuthService
from app.database.repositories.feedbacks_repository import FeedbacksRepository
from app.database.repositories.registrations_repository import RegistrationsRepository
from app.constants.exceptions import Exceptions


class AttendeeAccessController:
    def __init__(
        self,
        feedbacks_repository: FeedbacksRepository,
        auth_service: AuthService,
        registrations_repository: RegistrationsRepository,
    ):
        self.registration_repository = registrations_repository
        self.auth_service = auth_service
        self.feedbacks_repository = feedbacks_repository

    def validate_creation_role(
        self,
        token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="/api/v1/signin"))],
    ):
        role = self.auth_service.validate_user(token)["role"]
        if role != "ATTENDEE":
            raise Exceptions.ROLE_ERROR.value

    async def verify_feedback_permission(
        self,
        token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="/api/v1/signin"))],
        feedback_id: UUID = Path(...),
    ):
        user_id = UUID(self.auth_service.validate_user(token)["sub"])
        feedback = await self.feedbacks_repository.get_one(feedback_id)
        if feedback.user_id != user_id:
            raise Exceptions.PERMISSION_ERROR.value

    async def verify_registration_permission(
        self,
        token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="/api/v1/signin"))],
        registration_id: UUID = Path(...),
    ):
        user_id = UUID(self.auth_service.validate_user(token)["sub"])
        registration = await self.registration_repository.get_one(registration_id)
        if registration.user_id != user_id:
            raise Exceptions.PERMISSION_ERROR.value
