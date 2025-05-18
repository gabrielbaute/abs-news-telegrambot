import asyncio
from src.bot import TelegramBot

async def main():
    bot = TelegramBot()
    result = await bot.send_book_of_the_day()
    print(result)

if __name__ == "__main__":
    asyncio.run(main())