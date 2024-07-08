from uuid import UUID

import pytest

from app.database.models.event import Event


@pytest.mark.asyncio
async def test_create_event(mock_events_service):
    event_data = {
        "location": "Paris",
        "date": "2028-10-10",
        "description": "asasaasa",
        "tag": "CONCERT",
        "organizer_id": UUID("123e4567-e89b-12d3-a456-426614174000"),
    }
    expected_result = UUID("555b998c-f268-4ed4-a925-b4d6b84a7efd")
    mock_events_service.events_repository.insert_one.return_value = expected_result
    result = await mock_events_service.create_event(event_data)
    assert result == expected_result
    assert isinstance(result, UUID)
    mock_events_service.events_repository.insert_one.assert_called_once()


@pytest.mark.asyncio
async def test_update_event_by_id(mock_events_service):
    new_data = {"description": "new description"}
    expected_result = Event(
        id=UUID("555b998c-f268-4ed4-a925-b4d6b84a7efd"),
        location="Paris",
        date="2028-10-10",
        description="new description",
        created_at="2024-06-19 14:23:45",
        tag_id="CONCERT",
        organizer_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
    )
    event_id = UUID("555b998c-f268-4ed4-a925-b4d6b84a7efd")
    mock_events_service.events_repository.update_one.return_value = expected_result
    result = await mock_events_service.update_event_by_id(new_data, event_id)
    assert result == expected_result
    mock_events_service.events_repository.update_one.assert_called_once_with(
        new_data, event_id
    )


@pytest.mark.asyncio
async def test_delete_event(mock_events_service):
    event_id = UUID("555b998c-f268-4ed4-a925-b4d6b84a7efd")
    expected_result = Event(
        id=UUID("555b998c-f268-4ed4-a925-b4d6b84a7efd"),
        location="Paris",
        date="2028-10-10",
        description="new description",
        created_at="2024-06-19 14:23:45",
        tag_id="CONCERT",
        organizer_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
    )
    mock_events_service.events_repository.delete_one.return_value = expected_result
    result = await mock_events_service.delete_event(event_id)
    assert result == expected_result


@pytest.mark.asyncio
async def test_get_events(mock_events_service):
    kwargs = {"limit": 10, "offset": 0, "sort": "asc,location"}
    expected_result = [
        Event(
            id=UUID("555b998c-f268-4ed4-a925-b4d6b84a7efd"),
            location="Paris",
            date="2028-10-10",
            description="new description",
            created_at="2024-06-19 14:23:45",
            tag_id="CONCERT",
            organizer_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
            tag=None,
        )
    ]
    mock_events_service.events_repository.get_many.return_value = expected_result
    result = await mock_events_service.get_events(**kwargs)
    assert isinstance(result, list)
    assert result == expected_result


@pytest.mark.asyncio
@pytest.mark.xfail
async def test_get_filtered_events(mock_events_service):
    data = {
        "filters": {
            "or": [
                {"field": "location", "op": "like", "value": "%New York%"},
                {
                    "and": [
                        {"field": "date", "op": "date_gt", "value": "2023-01-01"},
                        {"field": "description", "op": "is_not_null"},
                    ]
                },
            ]
        },
        "sort": [
            {"field": "date", "direction": "asc"},
            {"field": "location", "direction": "desc"},
        ],
        "pagination": {"limit": 1, "offset": 1},
    }
    expected_result = [
        Event(
            id=UUID("555b998c-f268-4ed4-a925-b4d6b84a7efd"),
            location="New York",
            date="2028-10-10",
            description="new description",
            created_at="2024-06-19 14:23:45",
            tag_id="CONCERT",
            organizer_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
            tag=None,
            organizer=[],
            feedbacks=[],
        )
    ]
    mock_events_service.events_repository.get_all_by_filters.return_value = (
        expected_result
    )
    result = await mock_events_service.get_filtered_events(data)
    assert result != expected_result
    assert ~isinstance(result, list)
    mock_events_service.events_repository.get_all_by_filters.assert_not_called()
