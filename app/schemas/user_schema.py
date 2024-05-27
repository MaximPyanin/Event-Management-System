from pydantic import BaseModel
from pydantic import EmailStr
from app.constants.roles import Roles


class UserCreationDto(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Roles
    # potom prosto tk eto enum table just insert role_id:role with it is nit enum as events myself to find by id th eveetn and then its instance to pass to rrelationships but with enum table directly to fk
