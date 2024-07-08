from uuid import UUID

import pytest

from app.database.models.feedback import Feedback


@pytest.mark.asyncio
async def test_create_feedback(mock_feedbacks_service):
    data = {
        "comment": "qwqwqw",
        "rating": 8.9,
        "event_id": UUID("1eea4266-451e-4f5d-9546-b3e5a671a26f"),
        "user_id": UUID("91b168c9-a44d-4306-a6d4-1cf6db2d2ff9"),
    }
    expected_result = UUID("09955f2c-d14a-4611-9621-e52b697fcdde")
    mock_feedbacks_service.feedback_repository.insert_one.return_value = expected_result
    result = await mock_feedbacks_service.create_feedback(data)
    assert result == expected_result
    assert isinstance(result, UUID)
    mock_feedbacks_service.feedback_repository.insert_one.assert_called()


@pytest.mark.asyncio
async def test_update_feedback(mock_feedbacks_service):
    new_data = {"comment": "trtrt", "rating": 9.7}
    feedback_id = UUID("09955f2c-d14a-4611-9621-e52b697fcdde")
    expected_result = Feedback(
        id=UUID("09955f2c-d14a-4611-9621-e52b697fcdde"),
        comment="trtrt",
        updated_at="2024-06-21 12:19:19.052732",
        rating=9.7,
        event_id=UUID("1eea4266-451e-4f5d-9546-b3e5a671a26f"),
        user_id=UUID("91b168c9-a44d-4306-a6d4-1cf6db2d2ff9"),
    )
    mock_feedbacks_service.feedback_repository.update_one.return_value = expected_result
    result = await mock_feedbacks_service.update_feedback(new_data, feedback_id)
    assert result == expected_result
    assert isinstance(result, Feedback)
    mock_feedbacks_service.feedback_repository.update_one.assert_called_once_with(
        new_data, feedback_id
    )


@pytest.mark.asyncio
async def test_delete_feedback(mock_feedbacks_service):
    id = UUID("09955f2c-d14a-4611-9621-e52b697fcdde")
    expected_result = Feedback(
        id=UUID("09955f2c-d14a-4611-9621-e52b697fcdde"),
        comment="trtrt",
        updated_at="2024-06-21 12:19:19.052732",
        rating=9.7,
        event_id=UUID("1eea4266-451e-4f5d-9546-b3e5a671a26f"),
        user_id=UUID("91b168c9-a44d-4306-a6d4-1cf6db2d2ff9"),
    )
    mock_feedbacks_service.feedback_repository.delete_one.return_value = expected_result
    result = await mock_feedbacks_service.delete_feedback(id)
    assert result == expected_result
    mock_feedbacks_service.feedback_repository.delete_one.assert_called_once()
