from uuid import UUID

from fastapi import HTTPException

from app.database.repositories.users_repository import UsersRepository
from app.utils.hash_service import HashService
from app.utils.jwt_service import JWTService


class AuthService:
    def __init__(self,users_repository: UsersRepository,jwt_service: JWTService):
        self.users_repository = users_repository
        self.jwt_service = jwt_service

    async def authenticate_user(self,username: str,password: str) -> tuple:
        user = await self.users_repository.get_one_by_username(username)
        if not user:
            raise HTTPException(
                   status_code=401,
                detail='Incorrect password or username',
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not HashService.check_password(password,user.password):
               raise HTTPException(
                   status_code=401,
                   detail='Incorrect password or username',
                   headers={"WWW-Authenticate": "Bearer"},
               )
        return user.id,user.role_id

    def create_access_token(self,id: UUID,role: str) -> str:
        return self.jwt_service.encode_jwt({'sub':id,'role':role})