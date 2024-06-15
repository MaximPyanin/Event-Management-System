from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.auth_service import AuthService
from app.schemas.refresh_schema import RefreshToken


class AuthorizationRouter:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service
        self.router = APIRouter(tags=["auth"], prefix="/api/v1")

    def get_router(self) -> APIRouter:
        self.router.post("/signin")(self.singin)
        self.router.post("/refresh")(self.refresh)
        return self.router

    async def singin(
        self, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
    ) -> dict:
        user_id, role = await self.auth_service.authenticate_user(
            form_data.username, form_data.password
        )
        access_token = self.auth_service.create_access_token(user_id, role)
        refresh_token = self.auth_service.create_refresh_token(user_id)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    async def refresh(self, refresh_token: RefreshToken) -> dict:
        user_id, role = await self.auth_service.get_by_refresh_token(
            refresh_token.refresh_token
        )
        return {
            "access_token": self.auth_service.create_access_token(user_id, role),
            "refresh_token":self.auth_service.create_refresh_token(user_id),
            "token_type": "bearer",
        }
