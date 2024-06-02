from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

class SmsSchedulerService:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.set()

    def set(self):
        return self.scheduler.add_job('self.send_sms', CronTrigger(minute="0", hour="8", day="*", month="*", day_of_week="*"))

    def start(self):
        return self.scheduler.start()

    def stop(self):
        return self.scheduler.shutdown()


