from pydantic import BaseModel
from pydantic import EmailStr
from app.constants.roles import Roles


class UserCreationDto(BaseModel):
    username: str
    email: EmailStr
    phone: str
    password: str
    role: Roles
