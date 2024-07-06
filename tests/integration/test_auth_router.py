from uuid import UUID
from tests.helper import get_access_token
import pytest


@pytest.mark.asyncio
@pytest.mark.skip
async def test_signup(integration_client):
    user_data = {
        "username": "new_userm",
        "password": "lfdfdfd",
        "email": "rere@gmail.com",
        "phone": "+213423423",
        "role": "ORGANIZER",
    }
    response = await integration_client.post("/api/v1/signup", json=user_data)
    print(response.json())
    assert response.status_code == 200
    assert isinstance(UUID(response.json()["user_id"]), UUID)


@pytest.mark.asyncio
async def test_signin(integration_client):
    form_data = {"username": "new_user", "password": "lfdfdfd"}
    response = await integration_client.post("/api/v1/signin", data=form_data)
    assert response.status_code == 200
    assert len(response.json()) == 3


@pytest.mark.asyncio
async def test_refresh(integration_client):
    data = await get_access_token(integration_client)
    print(data)
    response = await integration_client.post(
        "/api/v1/refresh", json={"refresh_token": data["refresh_token"]}
    )
    assert response.status_code == 200
    assert isinstance(UUID(response.json()["refresh_token"]), UUID)
    assert len(response.json()) == 3
