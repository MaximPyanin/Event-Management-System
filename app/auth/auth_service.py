import datetime
import uuid
from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError

from app.database.repositories.users_repository import UsersRepository
from app.utils.hash_service import HashService
from app.utils.jwt_service import JWTService
from app.constants.exceptions import Exceptions


class AuthService:
    def __init__(self, users_repository: UsersRepository, jwt_service: JWTService):
        self.users_repository = users_repository
        self.jwt_service = jwt_service

    @staticmethod
    def get_oauth2_bearer() -> OAuth2PasswordBearer:
        return OAuth2PasswordBearer("/api/v1/login")

    async def authenticate_user(self, username: str, password: str) -> tuple:
        user = await self.users_repository.get_one_by_username(username)
        if not user:
            raise Exceptions.AUTHENTICATION_ERROR.value
        if not HashService.check_password(password, user.password):
            raise Exceptions.AUTHENTICATION_ERROR.value
        return user.id, user.role_id

    def create_access_token(self, id: UUID, role: str) -> str:
        return self.jwt_service.encode_jwt({"sub": id, "role": role})

    def decode_access_token(self, token: str | bytes) -> dict:
        return self.jwt_service.decode_jwt(token)

    def validate_user(self, token: str = Depends(get_oauth2_bearer)) -> None:
        try:
            self.decode_access_token(token)
        except InvalidTokenError:
            raise Exceptions.AUTHENTICATION_ERROR.value

    async def create_refresh_token(self, user_id: UUID, expire_days: int = 30) -> UUID:
        refresh_token = uuid.uuid4()
        await self.users_repository.update_one(
            {
                "refresh_token": refresh_token,
                "expired_at": datetime.datetime.utcnow()
                + datetime.timedelta(days=expire_days),
            },
            user_id,
        )
        return refresh_token

    async def get_by_refresh_token(self, token: UUID) -> tuple:
        user = await self.users_repository.get_one_by_token(token)
        if not user:
            raise Exceptions.AUTHENTICATION_ERROR.value
        if user.expired_at <= datetime.datetime.utcnow():
            raise Exceptions.AUTHENTICATION_ERROR.value
        return user.id, user.role_id
