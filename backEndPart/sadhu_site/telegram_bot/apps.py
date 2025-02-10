import threading  # Для запуску бота в окремому потоці
from django.apps import AppConfig
from .secure import TELEGRAM_BOT_TOKEN


class TelegramBotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'telegram_bot'

    def ready(self):
        # Імпортуємо логіку запуску бота
        from .bot_runner import run_bot

        # Вставте токен вашого Telegram-бота
        token = TELEGRAM_BOT_TOKEN  # Замініть на токен вашого бота

        # Запускаємо бота в окремому потоці, щоб не блокувати сервер
        bot_thread = threading.Thread(target=run_bot, args=(token,))
        bot_thread.start()
