import asyncio
import threading
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from telegram.error import Conflict
from .views import *
from telegram import Bot


async def send_order_notification(order):
    """
    Асинхронна функція для надсилання сповіщення адміністраторам про нове замовлення.
    """
    from .secure import TELEGRAM_BOT_TOKEN
    from admin_panel.models import SystemUser as User
    from django.db.models import Q

    ADMIN_CHAT_IDS = await sync_to_async(list)(
        User.objects.filter(
            Q(access_level='admin') | Q(access_level='super')
        ).values_list('user_id', flat=True)
    )

    bot = Bot(token=TELEGRAM_BOT_TOKEN)  # Ініціалізація Telegram бота
    message = (
        f"<b>🛒 ЗАМОВЛЕННЯ #{order.id} — {order.product_id.name}</b>\n\n"
        f"<b>👤 Клієнт:</b>\n"
        f"Ім'я: <i>{order.customer_id.name} {order.customer_id.surname}</i>\n"
        f"Телефон: <i>{order.customer_id.phone}</i>\n\n"
        f"<b>🚚 Доставка:</b> <i>{order.address} #{order.post}</i>\n"
        f"<b>💰 Сума:</b> <i>{order.price} грн</i>\n"
        f"{'🔔 <b>Потрібно зателефонувати клієнту!</b>' if order.status == 'should_call' else ''}\n"
        f"<b>🕒 Час:</b> {order.created_at.strftime('%d.%m.%Y %H:%M')}"
    )

    # Надсилаємо повідомлення всім адміністраторам
    for admin_id in ADMIN_CHAT_IDS:
        try:
            await bot.send_message(chat_id=admin_id, text=message, parse_mode='HTML')
        except Exception as e:
            print(f"Помилка під час надсилання повідомлення адміністратору {admin_id}: {e}")


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
        app.add_handler(CommandHandler("manager", manager))
        app.add_handler(CommandHandler("tosend", to_send))

        # Зареєструйте обробник помилок
        app.add_error_handler(error_handler)

        # Запускаємо polling із drop_pending_updates=True
        loop.run_until_complete(app.run_polling(drop_pending_updates=True))

    # Запуск в окремому потоці
    thread = threading.Thread(target=bot_thread, daemon=True)
    thread.start()
