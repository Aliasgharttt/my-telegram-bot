import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from persiantools.jdatetime import JalaliDateTime
from config import TOKEN


# --- توابع دریافت اطلاعات ---

def get_currency():
    try:
        res = requests.get("https://api.exchangerate.host/latest?base=USD")
        data = res.json()
        usd = 1
        eur = data["rates"]["EUR"]
        return f"💵 دلار: {usd} USD\n💶 یورو: {eur:.2f} EUR"
    except:
        return "❌ خطا در دریافت قیمت ارز"


def get_gold():
    # اینجا می‌تونی بعداً API واقعی بزاری
    return "🥇 قیمت طلا: ۲,۳۵۰,۰۰۰ تومان"


def get_time_date():
    now = JalaliDateTime.now()
    return f"📅 تاریخ: {now.strftime('%Y/%m/%d')}\n⏰ ساعت: {now.strftime('%H:%M:%S')}"


# --- منوی شروع ---

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("💵 قیمت ارز", callback_data="currency")],
        [InlineKeyboardButton("🥇 قیمت طلا", callback_data="gold")],
        [InlineKeyboardButton("⏰ زمان و تاریخ", callback_data="time")],
        [InlineKeyboardButton("ℹ️ درباره ربات", callback_data="about")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("👇 یکی از گزینه‌ها رو انتخاب کن:", reply_markup=reply_markup)


# --- مدیریت دکمه‌ها ---

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == "currency":
        query.edit_message_text(get_currency())
    elif query.data == "gold":
        query.edit_message_text(get_gold())
    elif query.data == "time":
        query.edit_message_text(get_time_date())
    elif query.data == "about":
        query.edit_message_text("🤖 این ربات قیمت لحظه‌ای دلار، یورو، طلا + تاریخ و ساعت ایران رو نشون میده.")


# --- اجرای ربات ---

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
