import logging
import requests
import random
from datetime import datetime
import pytz
from persiantools.jdatetime import JalaliDate
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ----------------- تنظیمات لاگ -----------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ----------------- لیست API ها -----------------
APIS = [
    "https://api.navasan.tech/latest/?api_key=free",
    "https://api.tgju.online/v1/data/sana/json",
    "https://alanchand.com/media/api"
]

# ----------------- گرفتن قیمت از API -----------------
def get_prices():
    url = random.choice(APIS)
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()

        # هر API فرمتش متفاوته → اینجا ساده‌سازی کردم
        if "usd" in str(data).lower():  # اگر دلار پیدا شد
            dollar = data.get("usd", {}).get("p", "نامشخص")
            euro = data.get("eur", {}).get("p", "نامشخص")
            gold = data.get("gold_18k", {}).get("p", "نامشخص")
        elif "sana" in str(data).lower():
            dollar = data["sana"]["price"].get("usd", "نامشخص")
            euro = data["sana"]["price"].get("eur", "نامشخص")
            gold = "نامشخص"
        else:  # fallback
            dollar = data.get("usd", "نامشخص")
            euro = data.get("eur", "نامشخص")
            gold = data.get("gold", "نامشخص")

        return dollar, euro, gold
    except Exception as e:
        logging.error(f"API Error: {e}")
        return "خطا", "خطا", "خطا"

# ----------------- شروع ربات -----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💵 قیمت دلار", callback_data="dollar")],
        [InlineKeyboardButton("💶 قیمت یورو", callback_data="euro")],
        [InlineKeyboardButton("🏅 قیمت طلا", callback_data="gold")],
        [InlineKeyboardButton("📅 تاریخ شمسی", callback_data="date")],
        [InlineKeyboardButton("⏰ ساعت تهران", callback_data="time")],
        [InlineKeyboardButton("🎲 تاس", callback_data="dice")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("سلام 👋\nلطفا یکی از گزینه‌های زیر رو انتخاب کن:", reply_markup=reply_markup)

# ----------------- پاسخ به دکمه‌ها -----------------
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    dollar, euro, gold = get_prices()

    if query.data == "dollar":
        await query.edit_message_text(text=f"💵 قیمت لحظه‌ای دلار: {dollar} تومان")
    elif query.data == "euro":
        await query.edit_message_text(text=f"💶 قیمت لحظه‌ای یورو: {euro} تومان")
    elif query.data == "gold":
        await query.edit_message_text(text=f"🏅 قیمت لحظه‌ای طلا: {gold} تومان")
    elif query.data == "date":
        today = JalaliDate.today()
        await query.edit_message_text(text=f"📅 تاریخ امروز (شمسی): {today}")
    elif query.data == "time":
        tehran = pytz.timezone("Asia/Tehran")
        now = datetime.now(tehran).strftime("%H:%M:%S")
        await query.edit_message_text(text=f"⏰ ساعت فعلی تهران: {now}")
    elif query.data == "dice":
        dice = random.randint(1, 6)
        await query.edit_message_text(text=f"🎲 تاس: {dice}")

# ----------------- اجرای ربات -----------------
def main():
    from config import TOKEN  # توکن از فایل config.py خونده میشه
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()

if __name__ == "__main__":
    main()
