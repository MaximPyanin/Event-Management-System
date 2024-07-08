import datetime
import uuid
from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.exc import NoResultFound

from app.database.repositories.users_repository import UsersRepository
from app.utils.hash_service import HashService
from app.utils.jwt_service import JWTService
from app.constants.exceptions import Exceptions


class AuthService:
    def __init__(self, users_repository: UsersRepository, jwt_service: JWTService):
        self.users_repository = users_repository
        self.jwt_service = jwt_service

    async def authenticate_user(self, username: str, password: str) -> tuple:
        try:
            user = await self.users_repository.get_one_by_username(username)
        except NoResultFound:
            raise Exceptions.AUTHENTICATION_ERROR.value
        if not HashService.check_password(password, user.password.encode()):
            raise Exceptions.AUTHENTICATION_ERROR.value
        return user.id, user.role_id

    def create_access_token(self, id: UUID, role: str) -> str:
        return self.jwt_service.encode_jwt({"sub": str(id), "role": role.value})

    def decode_access_token(self, token: str | bytes) -> dict:
        return self.jwt_service.decode_jwt(token)

    def validate_user(
        self,
        token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="/api/v1/signin"))],
    ) -> dict:
        try:
            self.decode_access_token(token)
        except InvalidTokenError:
            raise Exceptions.TOKEN_AUTHENTICATION_ERROR.value
        return self.decode_access_token(token)

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
        try:
            user = await self.users_repository.get_one_by_token(token)
        except NoResultFound:
            raise Exceptions.TOKEN_AUTHENTICATION_ERROR.value
        if user.expired_at <= datetime.datetime.utcnow():
            raise Exceptions.TOKEN_AUTHENTICATION_ERROR.value
        return user.id, user.role_id
