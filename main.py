import logging
import os
import random
import datetime
from googletrans import Translator
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Логирование
logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")
translator = Translator()

# Загружаем цитаты
with open("quotes.txt", "r", encoding="utf-8") as f:
    quotes = [line.strip() for line in f if line.strip()]

# Храним последнюю отправленную цитату
last_quote = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я буду каждый день в 10:00 отправлять тебе цитату.")

async def send_daily_quote(context: ContextTypes.DEFAULT_TYPE):
    global last_quote
    last_quote = random.choice(quotes)
    
    keyboard = [
        [InlineKeyboardButton("Перевести", callback_data="translate")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await context.bot.send_message(chat_id=os.getenv("CHAT_ID"), text=last_quote, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    global last_quote

    if query.data == "translate" and last_quote:
        translated = translator.translate(last_quote, dest="en").text
        await query.edit_message_text(f"{last_quote}\n\nПеревод: {translated}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Планировщик
    scheduler = AsyncIOScheduler(timezone="Asia/Dushanbe")
    scheduler.add_job(send_daily_quote, 'cron', hour=10, minute=0, args=[app.bot])
    scheduler.start()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
