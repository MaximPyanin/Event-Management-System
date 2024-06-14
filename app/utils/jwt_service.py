from datetime import timedelta, datetime

import jwt

from app.services.config_service import AppConfig


class JWTService:
    def __init__(self, config: AppConfig):
        self.config = config

    def __get_key(self, *args) -> bytes:
        if args[0] == "private":
            with open(self.config.PRIVATE_KEY_PATH, "rb") as file:
                return file.read()
        else:
            with open(self.config.PUBLIC_KEY_PATH, "rb") as file:
                return file.read()

    def encode_jwt(self, payload: dict, expire_minutes: int = 15) -> str:
        payload.update({"exp": datetime.utcnow() + timedelta(minutes=expire_minutes)})
        return jwt.encode(payload, self.__get_key("private"), algorithm="RS256")

    def decode_jwt(self, token: bytes | str) -> dict:
        return jwt.decode(token, self.__get_key("public"), algorithms=["RS256"])
