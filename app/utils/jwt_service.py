from datetime import timedelta, datetime

import jwt

from app.services.config_service import AppConfig


class JWTService:
    def __init__(self, config: AppConfig):
        self.config = config

    def encode_jwt(self, payload: dict, expire_minutes: int = 15) -> str:
        payload.update({"exp": datetime.utcnow() + timedelta(minutes=expire_minutes)})
        return jwt.encode(payload, self.config.PRIVATE_KEY, algorithm="RS256")

    def decode_jwt(self, token: bytes | str) -> dict:
        return jwt.decode(token, self.config.PUBLIC_KEY, algorithms=["RS256"])
