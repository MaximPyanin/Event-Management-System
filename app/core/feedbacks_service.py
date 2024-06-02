from uuid import UUID

from app.database.repositories.feedbacks_repository import FeedbacksRepository


class FeedbacksService:
    def __init__(self,feedback_repository:FeedbacksRepository):
        self.feedback_repository = feedback_repository

    async def create_feedback(self,data: dict) -> UUID:
        res = await self.feedback_repository.insert_one(data)
        return res.id

    async def update_feedback(self,new_data: dict,id: UUID):
        return await self.feedback_repository.update_one(new_data,id)

    async def delete_feedback(self,id: UUID):
        return await self.feedback_repository.delete_one(id)