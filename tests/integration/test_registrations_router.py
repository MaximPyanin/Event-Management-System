from uuid import UUID

import pytest


@pytest.mark.asyncio
@pytest.mark.xfail
async def test_create_registration(integration_client):
    response = await integration_client.post(
        "/api/v1/registrations", data={"user_id": UUID(""), "event_id": UUID("")}
    )
    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Bearer"
    assert response.json()["detail"] == ""
