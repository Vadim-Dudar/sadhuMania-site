# telegram_bot/apps.py

from django.apps import AppConfig
from .secure import TELEGRAM_BOT_TOKEN
from .bot_runner import run_bot


class TelegramBotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'telegram_bot'

    def ready(self):
        """Фоновий запуск Telegram-бота разом із Django"""
        run_bot(TELEGRAM_BOT_TOKEN)
