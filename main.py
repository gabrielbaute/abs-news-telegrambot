import asyncio
from src.bot import BookScheduler

async def main():
    scheduler = BookScheduler()
    scheduler.start()
    
    # Mantén el script en ejecución
    try:
        while True:
            await asyncio.sleep(3600)  # Evita que el script termine
    except KeyboardInterrupt:
        scheduler.shutdown()

if __name__ == "__main__":
    asyncio.run(main())