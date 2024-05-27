import asyncio

from twilio.rest import Client
from twilio.rest.api.v2010.account.message import MessageInstance
from twilio.http.async_http_client import AsyncTwilioHttpClient

from app.services.config_service import AppConfig
from app.constants.notifications import Notifications


class SmsService:
    def __init__(self, config: AppConfig):
        self.config = config

    async def send_sms(self, number: str) -> MessageInstance:
        async with AsyncTwilioHttpClient() as session:
            client = Client(
                self.config.ACCOUNT_SID, self.config.AUTH_TOKEN, http_client=session
            )
            return await client.messages.create_async(
                from_=self.config.SENDER_PHONE, body=Notifications.sms_body, to=number
            )
