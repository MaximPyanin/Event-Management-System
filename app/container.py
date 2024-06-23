import os

from dependency_injector.containers import DeclarativeContainer
from dependency_injector import providers

from app.api.api_handler import APIHandler
from app.auth.attendee_access_controller import AttendeeAccessController
from app.auth.auth_router import AuthRouter
from app.auth.auth_service import AuthService
from app.auth.organizer_access_controller import OrganizerAccessController
from app.core.events_service import EventsService
from app.core.feedbacks_service import FeedbacksService
from app.core.registrations_service import RegistrationsService
from app.core.users_service import UsersService
from app.database.db import DB
from app.database.repositories.events_repository import EventsRepository
from app.database.repositories.feedbacks_repository import FeedbacksRepository
from app.database.repositories.registrations_repository import RegistrationsRepository
from app.database.repositories.users_repository import UsersRepository
from app.notifications.email_service import EmailService
from app.services.config_service import AppConfig
from app.services.logger_service import LoggerService

from app.api.events_router import EventsRouter
from app.api.feedbacks_router import FeedbacksRouter
from app.api.healthcheck_router import HealthcheckRouter
from app.api.registrations_router import RegistrationsRouter


from app.sockets.crypto_service import CryptoService
from app.sockets.websocket_router import WebsocketRouter
from app.sockets.websocket_service import WebsocketService
from app.utils.jwt_service import JWTService
from app.notifications.sms_scheduler_service import SmsSchedulerService
from app.notifications.sms_service import SmsService
from app.utils.query_builder import QueryBuilder


class Container(DeclarativeContainer):
    config = providers.Factory(AppConfig, env=os.environ)
    logger_service = providers.Singleton(LoggerService, config)
    jwt_service = providers.Factory(JWTService, config)
    db = providers.Singleton(DB, config)
    query_builder = providers.Factory(QueryBuilder, db)
    websocket_service = providers.Singleton(WebsocketService)
    crypto_service = providers.Singleton(CryptoService, websocket_service)
    websocket_router = providers.Singleton(WebsocketRouter, crypto_service)
    email_service = providers.Factory(EmailService, config)
    sms_scheduler_service = providers.Singleton(SmsSchedulerService)
    events_repository = providers.Factory(EventsRepository, db)
    registrations_repository = providers.Factory(RegistrationsRepository, db)
    users_repository = providers.Factory(UsersRepository, db)
    users_service = providers.Factory(UsersService, users_repository)
    registration_service = providers.Factory(
        RegistrationsService, registrations_repository
    )
    feedbacks_repository = providers.Factory(FeedbacksRepository, db)
    feedbacks_service = providers.Factory(FeedbacksService, feedbacks_repository)
    events_service = providers.Factory(EventsService, events_repository, query_builder)
    auth_service = providers.Factory(AuthService, users_repository, jwt_service)
    attendee_access_controller = providers.Factory(
        AttendeeAccessController,
        feedbacks_repository,
        auth_service,
        registrations_repository,
    )
    organizer_access_controller = providers.Factory(
        OrganizerAccessController,
        events_repository,
        auth_service,
    )
    auth_router = providers.Singleton(AuthRouter, auth_service, users_service)
    registration_router = providers.Singleton(
        RegistrationsRouter,
        email_service,
        registration_service,
        users_service,
        attendee_access_controller,
        auth_service,
    )
    healthcheck_router = providers.Singleton(HealthcheckRouter)
    feedback_router = providers.Singleton(
        FeedbacksRouter,
        feedbacks_service,
        auth_service,
        attendee_access_controller,
    )
    event_router = providers.Singleton(
        EventsRouter,
        events_service,
        auth_service,
        organizer_access_controller,
    )
    sms_service = providers.Factory(SmsService, config, events_repository)
    api_handler = providers.Singleton(
        APIHandler,
        event_router,
        logger_service,
        websocket_router,
        feedback_router,
        healthcheck_router,
        registration_router,
        sms_scheduler_service,
        auth_router,
        sms_service,
    )
