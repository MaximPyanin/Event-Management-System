from uuid import UUID

import pytest


@pytest.mark.asyncio
async def test_create_registration(integration_client):
    response = await integration_client.post(
        "/api/v1/registrations",
        data={
            "user_id": UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"),
            "event_id": UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"),
        },
    )
    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Bearer"
    assert response.json()["detail"] == "Invalid token"
