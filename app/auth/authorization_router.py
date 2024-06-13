from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.auth_service import AuthService


class AuthorizationRouter:
    def __init__(self,auth_service:AuthService):
        self.auth_service = auth_service
        self.router = APIRouter(tags=["auth"])

    def get_router(self) -> APIRouter:
        self.router.post('/signin')(self.login)
        return self.router

    async def login(self,form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> dict:
        user_id,role = await self.auth_service.authenticate_user(form_data.username,form_data.password)
        access_token = self.auth_service.create_access_token(user_id,role)
        return {'access_token':access_token,'refresh_token':''}


