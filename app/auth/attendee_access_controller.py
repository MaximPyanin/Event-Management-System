from uuid import UUID

from fastapi import Path

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

    def validate_creation_role(self):
        role = self.auth_service.validate_user()["role"]
        if role.value != "ATTENDEE":
            raise Exceptions.ROLE_ERROR.value

    async def verify_feedback_permission(self, feedback_id: UUID = Path(...)):
        user_id = self.auth_service.validate_user()["sub"]
        feedback = await self.feedbacks_repository.get_one(feedback_id)
        if feedback.user_id != user_id:
            raise Exceptions.PERMISSION_ERROR.value

    async def verify_registration_permission(self, registration_id: UUID = Path(...)):
        user_id = self.auth_service.validate_user()["sub"]
        registration = await self.registration_repository.get_one(registration_id)
        if registration.user_id != user_id:
            raise Exceptions.PERMISSION_ERROR.value
