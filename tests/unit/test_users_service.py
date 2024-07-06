from uuid import UUID

import pytest
from sqlalchemy.exc import NoResultFound

from app.database.models.user import User
from app.constants.user_roles import UserRoles

@pytest.mark.asyncio
async def test_create_user(mock_users_service):
    user_data = {
        "username": "testman",
        "email": "maximpyanin@gmail.com",
        "phone": "+194344544",
        "password": "nuinuinui09j",
        "role": UserRoles.ORGANIZER,
    }
    expected_result = UUID("1b44ed96-5595-457a-b119-736e4c0fa163")
    mock_users_service.users_repository.get_one_by_username.side_effect = NoResultFound
    mock_users_service.users_repository.insert_one.return_value = expected_result
    result = await mock_users_service.create_user(user_data)
    assert result == expected_result
    assert isinstance(result, UUID)
    mock_users_service.users_repository.get_one_by_username.assert_called()
    mock_users_service.users_repository.insert_one.assert_called()


@pytest.mark.asyncio
@pytest.mark.xfail
async def test_get_email(mock_users_service):
    user_id = UUID("1b44ed96-5595-457a-b119-736e4c0fa163")
    mock_users_service.users_repository.get_one.return_value = User(
        id=UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"),
        username="johndoe",
        email="johndoe@example.com",
        phone="+1234567890",
        password=b"securepassword",
        refresh_token=UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"),
        expired_at="2024-07-21 14:23:45.678912",
        role_id="ORGANIZER",
    )
    result = await mock_users_service.get_email(user_id)
    assert result != "johndoe@example.com"
    assert ~isinstance(result, str)
    mock_users_service.users_repository.get_one.assert_not_called()
