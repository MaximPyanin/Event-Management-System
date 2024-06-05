from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.notifications.sms_service import SmsService


class SmsSchedulerService:
    def __init__(self, sms_service: SmsService):
        self.scheduler = AsyncIOScheduler()
        self.set()
        self.sms_service = sms_service

    def set(self):
        return self.scheduler.add_job(
            self.sms_service.send_reminder,
            CronTrigger(minute="0", hour="8", day="*", month="*", day_of_week="*"),
        )

    def start(self):
        return self.scheduler.start()

    def stop(self):
        return self.scheduler.shutdown()
