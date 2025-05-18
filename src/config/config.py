"""Variables de configuración del proyecto."""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Clase de configuración del proyecto."""

    """Audiobookshelf API configuration."""
    SERVER_URL = os.getenv('SERVER_URL', 'http://localhost:13378')
    USERNAME = os.getenv('USERNAME')
    API_KEY= os.getenv('API_KEY')

    """Telegram Bot configuration."""
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

    """Scheduler configuration."""
    SCHEDULER_TIME_HOUR = os.getenv('SCHEDULER_TIME_HOUR', '14')
    SCHEDULER_TIME_MINUTE = os.getenv('SCHEDULER_TIME_MINUTE', '54')