from enum import Enum

from fastapi import HTTPException


class Exceptions(Enum):
    AUTHENTICATION_ERROR = HTTPException(
        status_code=401,
        detail="Incorrect password or username",
        headers={"WWW-Authenticate": "Bearer"},
    )
    USERNAME_ERROR = HTTPException(status_code=400, detail="Username already taken")
