# telegram_bot/apps.py

from django.apps import AppConfig
from .secure import TELEGRAM_BOT_TOKEN
from .bot_runner import run_bot
import threading


class TelegramBotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'telegram_bot'

    def ready(self):
        """Фоновий запуск Telegram-бота разом із Django"""
        bot_thread = threading.Thread(target=run_bot, args=(TELEGRAM_BOT_TOKEN,))
        bot_thread.daemon = True
        bot_thread.start()
