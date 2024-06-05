from uuid import UUID

from app.database.repositories.registrations_repository import RegistrationsRepository


class RegistrationsService:
    def __init__(self, registration_repository: RegistrationsRepository):
        self.repository = registration_repository

    async def create_registration(self, data: dict) -> UUID:
        res = await self.repository.insert_one(**data)
        return res.id

    async def delete_registration(self, registration_id: UUID):
        return await self.repository.delete_one(registration_id)
