from app.core.users_service import UsersService
from app.schemas.user_schema import UserCreationDto
from fastapi import APIRouter


class UsersRouter:
    def __init__(self, users_service: UsersService):
        self.users_service = users_service
        self.router = APIRouter(prefix="/api/v1", tags=["registration"])

    def get_router(self) -> APIRouter:
        self.router.post("/register")(self.register)
        return self.router

    async def register(self, user_dto: UserCreationDto) -> dict:
        user_id = await self.users_service.create_user(user_dto.model_dump())
        return {"user_id": user_id}
