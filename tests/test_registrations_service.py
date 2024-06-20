import pytest
from uuid import UUID
from app.database.models.registration import Registration
@pytest.mark.asyncio
async def test_create_registration(mock_registrations_service):
    data = {'event_id':'555b998c-f268-4ed4-a925-b4d6b84a7efd','user_id':'555b998c-f268-4ed4-a925-b4d6b84a3efd'}
    expected_result = '523b998c-f268-4ed4-a925-b4d6b84a7efd'
    mock_registrations_service.repository.insert_one.return_value = expected_result
    result = await mock_registrations_service.create_registration(data)
    assert result == expected_result
    assert isinstance(result,UUID
    mock_registrations_service.repository.insert_one.assert_called()


@pytest.mark.asyncio
async def test_delete_registration(mock_registrations_service):
    registration_id = "523b998c-f268-4ed4-a925-b4d6b84a7efd"
    expected_result = Registration(id='523b998c-f268-4ed4-a925-b4d6b84a7efd',user_id='555b998c-f268-4ed4-a925-b4d6b84a3efd',event_id='555b998c-f268-4ed4-a925-b4d6b84a7efd',)
    mock_registrations_service.repository.delete_one.return_value = expected_result
    result = await mock_registrations_service.delete_registration(registration_id)
    assert result == expected_result

