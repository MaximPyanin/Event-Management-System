from uuid import UUID

from app.auth.auth_service import AuthService
from app.auth.attendee_access_controller import AttendeeAccessController
from app.core.feedbacks_service import FeedbacksService
from app.schemas.feedback_schema import FeedbackCreationDto, FeedbackUpdateDto
from fastapi import APIRouter, Depends


class FeedbacksRouter:
    def __init__(
        self,
        feedbacks_service: FeedbacksService,
        auth_service: AuthService,
        attendee_access_controller: AttendeeAccessController,
    ):
        self.feedbacks_service = feedbacks_service
        self.attendee_access_controller = attendee_access_controller
        self.auth_service = auth_service
        self.router = APIRouter(
            prefix="/api/v1/feedbacks",
            tags=["feedbacks"],
            dependencies=[Depends(self.auth_service.validate_user)],
        )

    def get_router(self) -> APIRouter:
        self.router.post(
            "/",
            dependencies=[
                Depends(self.attendee_access_controller.validate_creation_role)
            ],
        )(self.create_feedback)
        self.router.put(
            "/{feedback_id}",
            dependencies=[
                Depends(self.attendee_access_controller.verify_feedback_permission)
            ],
        )(self.update_feedback)
        self.router.delete(
            "/{feedback_id}",
            dependencies=[
                Depends(self.attendee_access_controller.verify_feedback_permission)
            ],
        )(self.delete_feedback)
        return self.router

    async def create_feedback(self, feedback: FeedbackCreationDto):
        res = await self.feedbacks_service.create_feedback(feedback.model_dump())
        return {"feedback_id": res}

    async def update_feedback(self, feedback_id: UUID, feedback: FeedbackUpdateDto):
        return await self.feedbacks_service.update_feedback(
            feedback.model_dump(), feedback_id
        )

    async def delete_feedback(self, feedback_id: UUID):
        return await self.feedbacks_service.delete_feedback(feedback_id)
