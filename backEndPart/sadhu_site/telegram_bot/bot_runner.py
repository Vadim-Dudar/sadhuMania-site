# telegram_bot/bot_runner.py

import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from .views import start, handle_message


async def run_async_bot(token):
    """Асинхронний запуск Telegram-бота"""
    # Ініціалізація програми
    app = ApplicationBuilder().token(token).build()

    # Реєстрація обробників
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Виконуємо polling
    await app.run_polling()


def run_bot(token):
    """Синхронний запуск Telegram-бота (з урахуванням подій)"""
    try:
        # Отримуємо вже існуючу подію (або створюємо нову, якщо її немає)
        loop = asyncio.get_running_loop()
    except RuntimeError:  # Немає активного циклу
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # Запускаємо асинхронну функцію у вже існуючому циклі
    loop.create_task(run_async_bot(token))
