import asyncio
from src.bot import BookScheduler
from src.config import setup_logging

logger = setup_logging()

async def main():
    logger.info("Iniciando aplicación...")

    scheduler = BookScheduler()
    scheduler.start()
    
    try:
        while True:
            await asyncio.sleep(3600)
    
    except KeyboardInterrupt:
        scheduler.shutdown()

if __name__ == "__main__":
    asyncio.run(main())