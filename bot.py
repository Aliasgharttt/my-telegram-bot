import logging
import requests
import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from persiantools.jdatetime import JalaliDateTime
import pytz
import os

# لاگ برای دیباگ
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# توکن رو از محیط بگیر
TOKEN = os.getenv("TOKEN")

# --- /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💵 قیمت دلار", callback_data="usd"),
         InlineKeyboardButton("🥇 قیمت طلا", callback_data="gold")],
        [InlineKeyboardButton("💶 قیمت یورو", callback_data="eur"),
         InlineKeyboardButton("🎲 تاس", callback_data="dice")],
        [InlineKeyboardButton("⏰ ساعت", callback_data="time"),
         InlineKeyboardButton("📅 تاریخ شمسی", callback_data="date")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("سلام 👋 یکی از گزینه‌ها رو انتخاب کن:", reply_markup=reply_markup)

# --- کال‌بک‌ها ---
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "usd":
        price = get_price("usd")
        await query.edit_message_text(f"💵 قیمت دلار: {price} تومان")

    elif query.data == "gold":
        price = get_price("gold")
        await query.edit_message_text(f"🥇 قیمت طلا: {price} تومان")

    elif query.data == "eur":
        price = get_price("eur")
        await query.edit_message_text(f"💶 قیمت یورو: {price} تومان")

    elif query.data == "dice":
        num = random.randint(1, 6)
        await query.edit_message_text(f"🎲 عدد تاس: {num}")

    elif query.data == "time":
        tz = pytz.timezone("Asia/Tehran")
        now = JalaliDateTime.now(tz)
        await query.edit_message_text(f"⏰ ساعت: {now.strftime('%H:%M:%S')}")

    elif query.data == "date":
        tz = pytz.timezone("Asia/Tehran")
        now = JalaliDateTime.now(tz)
        await query.edit_message_text(f"📅 تاریخ: {now.strftime('%Y/%m/%d')}")

# --- گرفتن قیمت ---
def get_price(kind):
    urls = {
        "usd": "https://api.exchangerate.host/latest?base=USD&symbols=IRR",
        "eur": "https://api.exchangerate.host/latest?base=EUR&symbols=IRR",
        "gold": "https://api.exchangerate.host/latest?base=XAU&symbols=USD"
    }
    try:
        r = requests.get(urls[kind], timeout=10)
        data = r.json()
        return list(data["rates"].values())[0]
    except Exception:
        return "خطا در دریافت قیمت"

# --- /about ---
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 ساخته شده توسط دوست خوبت 🌹")

# --- main ---
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()

if __name__ == "__main__":
    main()
