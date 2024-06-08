from contextlib import asynccontextmanager

from typing import AsyncGenerator

from fastapi.middleware.cors import CORSMiddleware
from app.api.events_router import EventsRouter
from app.api.feedbacks_router import FeedbacksRouter
from app.api.healthcheck_router import HealthcheckRouter
from app.api.registrations_router import RegistrationsRouter
from app.api.users_router import UsersRouter
from fastapi import FastAPI

from app.notifications.sms_scheduler_service import SmsSchedulerService
from app.notifications.sms_service import SmsService

class APIHandler:
    def __init__(
        self,
        events_router: EventsRouter,
        feedback_router: FeedbacksRouter,
        healthcheck_router: HealthcheckRouter,
        registrations_router: RegistrationsRouter,
        users_router: UsersRouter,
        scheduler_service: SmsSchedulerService,
        sms_service: SmsService
    ):
        self.events_router = events_router
        self.feedback_router = feedback_router
        self.sms_service = sms_service
        self.healthcheck_router = healthcheck_router
        self.registrations_router = registrations_router
        self.users_router = users_router
        self.app = FastAPI(
            title="Event-Management-System", lifespan=asynccontextmanager(self.lifespan)
        )
        self.scheduler_service = scheduler_service
        self.include_routers()

    def include_routers(self) -> None:
        self.app.include_router(self.users_router.get_router())
        self.app.include_router(self.registrations_router.get_router())
        self.app.include_router(self.healthcheck_router.get_router())
        self.app.include_router(self.feedback_router.get_router())
        self.app.include_router(self.events_router.get_router())
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins = 'https://domain.com',
            allow_credentials = True,
            allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
            allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                           "Authorization"],
        )

    async def lifespan(self, app: FastAPI) -> AsyncGenerator:
        self.scheduler_service.add_job(self.sms_service.send_reminder)
        self.scheduler_service.start()
        yield
        self.scheduler_service.stop()
