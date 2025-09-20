import os
import requests
import jdatetime
import pytz
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

# -----------------------------
# خواندن توکن از فایل
# -----------------------------
with open("token.txt", "r") as f:
    TOKEN = f.read().strip()

APP_NAME = "my-telegram-bot-r23l"   # 👈 اینو با اسم دقیق سرویس Render خودت عوض کن
PORT = int(os.environ.get("PORT", 8443))

# -----------------------------
# گرفتن قیمت‌ها از سایت tgju.org
# -----------------------------
def get_price(symbol):
    url = f"https://api.tgju.online/v1/market/indicator/summary-table-data/{symbol}"
    try:
        data = requests.get(url, timeout=5).json()
        return data["data"]["p"]
    except:
        return "خطا در دریافت قیمت"

def get_dollar():
    return get_price("price_dollar_rl")

def get_euro():
    return get_price("price_eur")

def get_gold():
    return get_price("sekee")

# -----------------------------
# زمان و تاریخ ایران
# -----------------------------
def get_datetime():
    tz = pytz.timezone("Asia/Tehran")
    now = jdatetime.datetime.now(tz)
    return now.strftime("%Y/%m/%d - %H:%M:%S")

# -----------------------------
# شروع ربات
# -----------------------------
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("💵 قیمت دلار", callback_data="dollar"),
         InlineKeyboardButton("💶 قیمت یورو", callback_data="euro")],
        [InlineKeyboardButton("🏅 قیمت طلا", callback_data="gold")],
        [InlineKeyboardButton("📅 تاریخ و ساعت", callback_data="datetime")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("سلام 👋\nیکی از گزینه‌ها رو انتخاب کن:", reply_markup=reply_markup)

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == "dollar":
        query.edit_message_text(f"💵 دلار: {get_dollar()} تومان")
    elif query.data == "euro":
        query.edit_message_text(f"💶 یورو: {get_euro()} تومان")
    elif query.data == "gold":
        query.edit_message_text(f"🏅 سکه: {get_gold()} تومان")
    elif query.data == "datetime":
        query.edit_message_text(f"📅 تاریخ و ساعت ایران:\n{get_datetime()}")

# -----------------------------
# ساخت اپ Flask برای وبهوک
# -----------------------------
app = Flask(__name__)
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CallbackQueryHandler(button_handler))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), updater.bot)
    dispatcher.process_update(update)
    return "ok"

@app.route("/")
def home():
    return "ربات فعال است ✅"

if __name__ == "__main__":
    updater.bot.set_webhook(f"https://{APP_NAME}.onrender.com/{TOKEN}")
    app.run(host="0.0.0.0", port=PORT)
