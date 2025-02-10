# telegram_bot/views.py

from telegram import Update
from telegram.ext import ContextTypes
from asgiref.sync import sync_to_async


async def is_allowed_user(chat_id):
    from admin_panel.models import BotUsers  # Імпортуємо модель

    # 1. Перевірити існування користувача в базі
    user_exists = await sync_to_async(BotUsers.objects.filter(user_id=chat_id).exists)()
    if user_exists:
        user = await sync_to_async(BotUsers.objects.get)(user_id=chat_id)
        return user

    return False



# Обробляємо команду /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await is_allowed_user(update.effective_user.id):
        await update.message.reply_text(f"Привіт {update.effective_user.first_name}! Ти успішно пройшов реєстрацію і маєш доступ до бота! 🥳")
    else:
        await update.message.reply_text(f"Привіт {update.effective_user.first_name}! Ти не зареєстрований у системі SadhuMania. Для того щоб тебе додали передай:")
        await update.message.reply_text(f"{update.effective_user.full_name}: {update.effective_user.id}")


# Обробляємо текстові повідомлення
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text  # Текстове повідомлення від користувача
    await update.message.reply_text(f"Ви сказали: {user_text}")
