from app.core.events_service import EventsService
from app.core.users_service import UsersService
from app.core.registrations_service import RegistrationsService
from app.core.feedbacks_service import FeedbacksService
import pytest
import os
from dotenv import load_dotenv

from app.database.repositories.events_repository import EventsRepository
from app.database.repositories.feedbacks_repository import FeedbacksRepository
from app.database.repositories.registrations_repository import RegistrationsRepository
from app.database.repositories.users_repository import UsersRepository
from app.utils.query_builder import QueryBuilder
from httpx import AsyncClient, ASGITransport
from app.main import app

load_dotenv()


@pytest.fixture
def mock_events_service(mocker):
    return EventsService(
        mocker.MagicMock(spec=EventsRepository), mocker.MagicMock(spec=QueryBuilder)
    )


@pytest.fixture
def mock_users_service(mocker):
    return UsersService(mocker.MagicMock(spec=UsersRepository))


@pytest.fixture
def mock_registrations_service(mocker):
    return RegistrationsService(mocker.MagicMock(spec=RegistrationsRepository))


@pytest.fixture
def mock_feedbacks_service(mocker):
    return FeedbacksService(mocker.MagicMock(spec=FeedbacksRepository))


@pytest.fixture
def integration_client():
    return AsyncClient(base_url=os.getenv("APP_URL"), transport=ASGITransport(app=app))


@pytest.fixture
async def login():
    credentials = await integration_client().post("/api/v1/login")
