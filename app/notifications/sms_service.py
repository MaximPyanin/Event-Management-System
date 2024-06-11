from twilio.rest import Client
from twilio.rest.api.v2010.account.message import MessageInstance
from twilio.http.async_http_client import AsyncTwilioHttpClient
import datetime

from app.database.repositories.events_repository import EventsRepository
from app.services.config_service import AppConfig
from app.constants.notifications import Notifications


class SmsService:
    def __init__(self, config: AppConfig, events_repository: EventsRepository):
        self.config = config
        self.events_repository = events_repository

    async def send_sms(self, number: str) -> MessageInstance:
        async with AsyncTwilioHttpClient() as session:
            client = Client(
                self.config.ACCOUNT_SID, self.config.AUTH_TOKEN, http_client=session
            )
            return await client.messages.create_async(
                from_=self.config.SENDER_PHONE, body=Notifications.SMS_BODY, to=number
            )

    async def send_reminder(self) -> int:
        coming_events = await self.events_repository.get_all(
            datetime.datetime.utcnow().date()
        )
        users = [user for event in coming_events for user in event.users]
        for user in users:
            await self.send_sms(user.phone)
        return len(users)
