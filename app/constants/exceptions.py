from enum import Enum

from fastapi import HTTPException


class Exceptions(Enum):
    AUTHENTICATION_ERROR = HTTPException(
        status_code=401, detail="Incorrect password or username"
    )
    TOKEN_AUTHENTICATION_ERROR = HTTPException(
        status_code=401,
        detail="Invalid token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    USERNAME_ERROR = HTTPException(status_code=400, detail="Username already taken")
    ROLE_ERROR = HTTPException(status_code=403, detail="Invalid role")
    PERMISSION_ERROR = HTTPException(
        status_code=403,
        detail="Access denied: You are not allowed to modify or delete events that do not belong to you.",
    )
