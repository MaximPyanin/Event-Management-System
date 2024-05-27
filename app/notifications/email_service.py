import asyncio
from sendgrid import SendGridAPIClient

from sendgrid.helpers.mail import *
from sendgrid.helpers.mail import Email, Mail, To
from app.services.config_service import AppConfig


class EmailService:
    def __init__(self, config: AppConfig):
        self.config = config
        self.__client = SendGridAPIClient(self.config.SENDGRID_API_KEY)
        self.sender = Email(self.config.SENDER_EMAIL)

    async def send_email(self, to_email: str, **kwargs):
        match kwargs.get("content"):
            case "event_registration":
                return asyncio.create_task(
                    self.__client.send(
                        Mail(
                            self.sender,
                            To(to_email),
                            subject="Registration Confirmation",
                            plain_text_content=PlainTextContent(
                                "Thank you for registering for our event! We're excited to have you join us. If you have any questions, feel free to reach out"
                            ),
                        )
                    )
                )
            case "event_cancellation":
                return asyncio.create_task(
                    self.__client.send(
                        Mail(
                            self.sender,
                            To(to_email),
                            subject="Event Cancellation",
                            plain_text_content=PlainTextContent(
                                "We regret to inform you that the event has been canceled. We apologize for any inconvenience this may cause. If you have any concerns or need further assistance, please don't hesitate to contact us."
                            ),
                        )
                    )
                )
