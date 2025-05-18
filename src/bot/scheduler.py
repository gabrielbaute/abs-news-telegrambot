import logging
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from src.bot.bot import TelegramBot
from src.config import Config

logger = logging.getLogger("AudiobookshelfBot.scheduler")

class BookScheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.bot = TelegramBot()
        logger.info("Inicializando scheduler...")

    async def send_daily_book(self):
        """Tarea programada: envía un libro al día."""
        try:
            logger.info("Ejecutando tarea programada: enviar libro del día")
            result = await self.bot.send_book_of_the_day()
            logger.info(result)
        except Exception as e:
            logger.error(f"Error en send_daily_book: {e}", exc_info=True)

    def start(self):
        """Programa el envío diario a las 9 AM."""
        trigger = CronTrigger(
            hour=Config.SCHEDULER_TIME_HOUR, 
            minute=Config.SCHEDULER_TIME_MINUTE
        )
        self.scheduler.add_job(
            self.send_daily_book,
            trigger=trigger,
            misfire_grace_time=60
        )
        self.scheduler.start()
        logger.info(
            f"Scheduler iniciado. Enviando libro a las "
            f"{Config.SCHEDULER_TIME_HOUR}:{Config.SCHEDULER_TIME_MINUTE} diariamente."
        )

    def shutdown(self):
        """Detiene el scheduler."""
        logger.info("Deteniendo scheduler...")
        self.scheduler.shutdown()