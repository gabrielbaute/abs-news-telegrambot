"""Variables de configuración del proyecto."""
import os
from dotenv import load_dotenv
from sqlalchemy.pool import NullPool

load_dotenv()

class Config:
    """Clase de configuración del proyecto."""

    """Audiobookshelf API configuration."""
    SERVER_URL = os.getenv('SERVER_URL', 'http://localhost:13378')
    USERNAME = os.getenv('USERNAME')
    API_KEY= os.getenv('API_KEY')

    """Logging configuration."""
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    """Telegram Bot configuration."""
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

    """Scheduler configuration."""
    SCHEDULER_TIME_HOUR = os.getenv('SCHEDULER_TIME_HOUR', '8')
    SCHEDULER_TIME_MINUTE = os.getenv('SCHEDULER_TIME_MINUTE', '15')
    TZ = os.getenv('TZ', 'America/Caracas')

    """Database configuration."""
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///src/instance/absbot.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    DB_ENGINE_OPTIONS = {
        'poolclass': NullPool,
        'connect_args': {'check_same_thread': False} if 'sqlite' in SQLALCHEMY_DATABASE_URI else {}
    }