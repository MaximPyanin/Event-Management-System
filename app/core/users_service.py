from uuid import UUID
from app.utils.hash_service import HashService
from app.database.repositories.users_repository import UsersRepository


class UsersService:
    def __init__(self, users_repository: UsersRepository):
        self.users_repository = users_repository

    async def create_user(self, user_data: dict) -> UUID:
        user_data["password"] = HashService.hash_password(user_data["password"])
        user_data.update({"role_id": user_data.pop("role")})
        res = await self.users_repository.create_user(user_data)
        return res.id
