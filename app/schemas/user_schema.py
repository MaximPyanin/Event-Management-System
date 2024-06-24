from pydantic import BaseModel
from pydantic import EmailStr
from app.constants.user_roles import UserRoles


class UserCreationDto(BaseModel):
    username: str
    email: EmailStr
    phone: str
    password: str
    role: UserRoles
