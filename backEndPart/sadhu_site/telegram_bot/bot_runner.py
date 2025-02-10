from telegram.ext import Application, CommandHandler  # Ensure 'python-telegram-bot' version is at least 20.0
from .views import start  # Імпорт команди /start з views.py


def run_bot(token):
    # Налаштування бота
    application = Application.builder().token(token).build()

    # Додавання команди /start
    application.add_handler(CommandHandler("start", start))

    # Старт бота
    application.run_polling()
