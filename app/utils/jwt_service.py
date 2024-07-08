from datetime import timedelta, datetime

import jwt

from app.services.config_service import AppConfig
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


class JWTService:
    def __init__(self, config: AppConfig):
        self.config = config
        self.private_key = serialization.load_pem_private_key(
            self.config.PRIVATE_KEY.encode().replace(b"\\n", b"\n"),
            password=None,
            backend=default_backend(),
        )
        self.public_key = serialization.load_pem_public_key(
            self.config.PUBLIC_KEY.encode().replace(b"\\n", b"\n"),
            backend=default_backend(),
        )

    def encode_jwt(self, payload: dict, expire_minutes: int = 15) -> str:
        payload.update({"exp": datetime.utcnow() + timedelta(minutes=expire_minutes)})
        return jwt.encode(payload, self.private_key, algorithm="RS256")

    def decode_jwt(self, token: bytes | str) -> dict:
        return jwt.decode(token, self.public_key, algorithms=["RS256"])
