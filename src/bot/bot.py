import os
import random
import logging
from telegram import Bot, InputMediaPhoto
from telegram.error import TelegramError

from src.core import AudiobookshelfAPI
from src.config import Config
from src.database import add_sent_book, was_book_sent

logger = logging.getLogger("AudiobookshelfBot.telegram")

class TelegramBot:
    def __init__(self):
        self.bot = Bot(token=Config.TELEGRAM_BOT_TOKEN)
        self.chat_id = Config.TELEGRAM_CHAT_ID
        logger.info("Bot de Telegram inicializado")

    async def send_book_of_the_day(self):
        try:
            api = AudiobookshelfAPI()
            libraries = api.get_libraries()
            if not libraries:
                msg = "❌ No se encontraron bibliotecas."
                logger.warning(msg)
                return msg

            books = api.get_all_books(libraries[0]["id"])
            if not books:
                msg = "❌ No se encontraron libros."
                logger.warning(msg)
                return msg

            # Filtro para no repetir
            unsent_books = [b for b in books if not was_book_sent(b["id"])]
            
            if not unsent_books:
                logger.warning("No hay libros no enviados disponibles")
                return "❌ Todos los libros ya fueron compartidos."

            book = random.choice(books)
            logger.debug(f"Libro seleccionado: ID={book['id']}")

            book_details = api.get_book_details(book["id"])
            if not book_details:
                msg = "❌ No se pudieron obtener los detalles del libro."
                logger.error(msg)
                return msg
            
            title = book_details.get("media", {}).get("metadata", {}).get("title", "Título desconocido")
            logger.info(f"Preparando envío del libro: '{title}' (ID: {book['id']})")
            
            formatted = api.format_book_message(book_details)

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

            add_sent_book(book_details)

            return "✅ Libro enviado con éxito!"
        
        except Exception as e:
            logger.critical(f"Error crítico al enviar mensaje a Telegram: {e}", exc_info=True)
            return f"❌ Error al enviar a Telegram: {e}"