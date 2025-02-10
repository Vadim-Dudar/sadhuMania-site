import asyncio
import threading
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from telegram.error import Conflict
from .views import start, handle_message


async def error_handler(update, context):
    """Обробник помилок для відстеження конфлікту"""
    if isinstance(context.error, Conflict):
        print("Conflict detected. Ignoring old updates.")
    else:
        print(f"Unexpected error: {context.error}")


def run_bot(token):
    """Запуск Telegram-бота в ізольованому потоці"""

    def bot_thread():
        # Створюємо і запускаємо новий подієвий цикл у потоці
        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        app = ApplicationBuilder().token(token).build()

        # Додайте ваші командні обробники
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        # Зареєструйте обробник помилок
        app.add_error_handler(error_handler)

        # Запускаємо polling із drop_pending_updates=True
        loop.run_until_complete(app.run_polling(drop_pending_updates=True))

    # Запуск в окремому потоці
    thread = threading.Thread(target=bot_thread, daemon=True)
    thread.start()
