import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from src.bot.bot import TelegramBot
from src.config import Config

class BookScheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.bot = TelegramBot()

    async def send_daily_book(self):
        """Tarea programada: envía un libro al día."""
        result = await self.bot.send_book_of_the_day()
        print(result)

    def start(self):
        """Programa el envío diario a las 9 AM."""
        trigger = CronTrigger(hour=Config.SCHEDULER_TIME_HOUR, minute=Config.SCHEDULER_TIME_MINUTE)
        self.scheduler.add_job(
            self.send_daily_book,
            trigger=trigger,
            misfire_grace_time=60
        )
        self.scheduler.start()
        print(f"🔄 Scheduler iniciado. Enviando libro a las {Config.SCHEDULER_TIME_HOUR}:{Config.SCHEDULER_TIME_MINUTE} diariamente.")

    def shutdown(self):
        """Detiene el scheduler."""
        self.scheduler.shutdown()