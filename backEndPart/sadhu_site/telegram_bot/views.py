from django.shortcuts import render

# Create your views here.
from telegram import Update
from telegram.ext import ContextTypes


# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обробка команди /start. Привітання користувача."""
    await update.message.reply_text(
        "Привіт! Я Telegram-бот для вашого сайту. Я допоможу вам керувати замовленнями.\n"
        "Спробуйте ввести команду, або надішліть мені повідомлення!"
    )

# Інші обробники ви можете додавати за такою ж структурою
