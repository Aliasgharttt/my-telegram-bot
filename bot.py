import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import requests
import pytz
import jdatetime
from datetime import datetime

TOKEN = "توکن_ربات_اینجا"

logging.basicConfig(level=logging.INFO)

# دکمه شروع
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💵 قیمت دلار/یورو", callback_data="currency")],
        [InlineKeyboardButton("🥇 قیمت طلا", callback_data="gold")],
        [InlineKeyboardButton("⏰ تاریخ و ساعت", callback_data="time")],
        [InlineKeyboardButton("ℹ️ درباره", callback_data="about")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🌍 یکی از گزینه‌ها رو انتخاب کن:", reply_markup=reply_markup)

# گرفتن اطلاعات
def get_currency():
    return "💵 دلار: 50,000 تومان\n💶 یورو: 55,000 تومان"

def get_gold():
    return "🥇 هر گرم طلا: 2,500,000 تومان"

def get_time_date():
    tehran_tz = pytz.timezone("Asia/Tehran")
    now = datetime.now(tehran_tz)
    jdate = jdatetime.datetime.fromgregorian(datetime=now)
    return f"⏰ {now.strftime('%H:%M:%S')}\n📅 {jdate.strftime('%Y/%m/%d')}"

# دکمه‌ها
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "currency":
        await query.edit_message_text(get_currency())
    elif query.data == "gold":
        await query.edit_message_text(get_gold())
    elif query.data == "time":
        await query.edit_message_text(get_time_date())
    elif query.data == "about":
        await query.edit_message_text("🤖 ربات نمایش لحظه‌ای قیمت دلار، یورو و طلا.")

# اجرای ربات
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()

if __name__ == "__main__":
    main()
