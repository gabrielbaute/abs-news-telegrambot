import os
import random
from telegram import Bot, InputMediaPhoto
from telegram.error import TelegramError
from src.core.audiobookshelf import AudiobookshelfAPI
from src.config.config import Config

class TelegramBot:
    def __init__(self):
        self.bot = Bot(token=Config.TELEGRAM_BOT_TOKEN)
        self.chat_id = Config.TELEGRAM_CHAT_ID

    async def send_book_of_the_day(self):
        api = AudiobookshelfAPI()
        libraries = api.get_libraries()
        if not libraries:
            return "❌ No se encontraron bibliotecas."

        books = api.get_all_books(libraries[0]["id"])
        if not books:
            return "❌ No se encontraron libros."
        
        random_book = random.choice(books)
        
        book_details = api.get_book_details(random_book["id"])
        if not book_details:
            return "❌ No se pudieron obtener los detalles del libro."

        formatted = api.format_book_message(book_details)
        
        try:
            if formatted["cover_url"]:
                await self.bot.send_photo(
                    chat_id=self.chat_id,
                    photo=formatted["cover_url"],
                    caption=formatted["message"],
                    parse_mode="Markdown"
                )
            else:
                await self.bot.send_message(
                    chat_id=self.chat_id,
                    text=formatted["message"],
                    parse_mode="Markdown"
                )
            return f"✅ Libro enviado con éxito: {formatted['title']}"
        except Exception as e:
            return f"❌ Error al enviar: {e}"