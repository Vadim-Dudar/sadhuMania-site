# telegram_bot/views.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from asgiref.sync import sync_to_async


async def is_allowed_user(chat_id):
    from admin_panel.models import SystemUser  # Імпортуємо модель

    # 1. Перевірити існування користувача в базі
    user_exists = await sync_to_async(SystemUser.objects.filter(user_id=chat_id).exists)()
    if user_exists:
        user = await sync_to_async(SystemUser.objects.get)(user_id=chat_id)
        return user

    return False



# Обробляємо команду /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await is_allowed_user(update.effective_user.id):
        await update.message.reply_text(f"Привіт {update.effective_user.first_name}! Ти успішно пройшов реєстрацію і маєш доступ до бота! 🥳")
    else:
        await update.message.reply_text(f"Привіт {update.effective_user.first_name}! Ти не зареєстрований у системі SadhuMania. Для того щоб тебе додали передай повідомлення нижче:")
        await update.message.reply_text(f"{update.effective_user.full_name}: {update.effective_user.id}", parse_mode='MarkdownV2')

async def manager(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from products.models import Order
    if await is_allowed_user(update.effective_user.id):
        for order in await sync_to_async(list)(Order.objects.filter(sent=False, manager=True)):
            message = (
                f"<b>ЗАМОВЛЕННЯ #{order.id} '{order.product}'</b>\n\n"
                f"Ім'я: {order.name} {order.surname}\n"
                f"Телефон: {order.phone}\n"
                f"Віділення: {order.address} {order.post}\n"
                f"Сума: {order.price} грн\n"
                f"Телефон: {order.phone}\n"
                f"{'⭕ Менеджеру треба набрати' if order.manager else ''}\n"
                f"{order.created_at.strftime('%d.%m.%Y %H:%M')}"
            )
            await update.message.reply_text(message, parse_mode='HTML')


async def to_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from products.models import Order
    if await is_allowed_user(update.effective_user.id):
        for order in await sync_to_async(list)(Order.objects.filter(sent=False)):
            message = (
                f"<b>ЗАМОВЛЕННЯ #{order.id} '{order.product}'</b>\n\n"
                f"Ім'я: {order.name} {order.surname}\n"
                f"Телефон: {order.phone}\n"
                f"Віділення: {order.address} {order.post}\n"
                f"Сума: {order.price} грн\n"
                f"Телефон: {order.phone}\n"
                f"{'⭕ Менеджеру треба набрати' if order.manager else ''}\n"
                f"{order.created_at.strftime('%d.%m.%Y %H:%M')}"
            )
            await update.message.reply_text(message, parse_mode='HTML')


# Обробляємо текстові повідомлення
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text  # Текстове повідомлення від користувача
    await update.message.reply_text(f"Ви сказали: {user_text}")
