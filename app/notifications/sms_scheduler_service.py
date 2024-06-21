from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger


from typing import Callable, Coroutine, Any


class SmsSchedulerService:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()

    def add_job(self, func: Callable[..., Any] | Coroutine[Any, Any, Any]):
        return self.scheduler.add_job(
            func,
            CronTrigger(minute="0", hour="8", day="*", month="*", day_of_week="*"),
        )

    def start(self):
        return self.scheduler.start()

    def stop(self):
        return self.scheduler.shutdown()
