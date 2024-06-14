from uuid import UUID

from app.auth.auth_service import AuthService
from app.core.feedbacks_service import FeedbacksService
from app.schemas.feedback_schema import FeedbackCreationDto, FeedbackUpdateDto
from fastapi import APIRouter, Depends


class FeedbacksRouter:
    def __init__(self, feedbacks_service: FeedbacksService, auth_service: AuthService):
        self.feedbacks_service = feedbacks_service
        self.auth_service = auth_service
        self.router = APIRouter(
            prefix="/api/v1/feedbacks",
            tags=["feedbacks"],
            dependencies=[Depends(self.auth_service.validate_user)],
        )

    def get_router(self) -> APIRouter:
        self.router.post("/")(self.create_feedback)
        self.router.put("/{feedback_id}")(self.update_feedback)
        self.router.delete("/{feedback_id}")(self.delete_feedback)
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
