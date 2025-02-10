# telegram_bot/views.py

from telegram import Update
from telegram.ext import ContextTypes


# Обробляємо команду /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я ваш Telegram-бот. Як я можу допомогти?")


# Обробляємо текстові повідомлення
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text  # Текстове повідомлення від користувача
    await update.message.reply_text(f"Ви сказали: {user_text}")
