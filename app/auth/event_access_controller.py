from uuid import UUID

from app.auth.auth_service import AuthService
from app.database.repositories.events_repository import EventsRepository
from app.database.repositories.users_repository import UsersRepository
from app.utils.jwt_service import JWTService
from app.constants.exceptions import Exceptions

class EventAccessController:
    def __init__(self,users_repository: UsersRepository,jwt_service: JWTService,auth_service: AuthService):
        self.users_repository = users_repository
        self.jwt_service = jwt_service
        self.auth_service = auth_service


    async def check_role_for_creation(self):
        user = await self.users_repository.get_one(self.auth_service.validate_user()['sub'])
        if user.role_id.value != "ORGANIZER":
            raise Exceptions.ROLE_ERROR.value

    async def check_update_delete_permission(self,event_id: UUID,user_id: UUID):
        user = await self.users_repository.get_one(user_id)
        for event in user.events:
            if event.id == event_id:
                return True
        raise Exceptions.PERMISSION_ERROR.value
