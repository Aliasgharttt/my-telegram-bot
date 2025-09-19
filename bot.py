import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
import requests
import jdatetime
import pytz
from bs4 import BeautifulSoup

# خواندن توکن از فایل token.txt
with open("token.txt", "r") as f:
    TOKEN = f.read().strip()

# فعال کردن لاگ برای رفع خطا
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# دریافت نرخ دلار و یورو از exchangerate.host
def get_currency():
    try:
        url = "https://api.exchangerate.host/latest?base=USD&symbols=IRR,EUR"
        r = requests.get(url).json()
        usd_to_irr = r["rates"]["IRR"]
        usd_to_eur = r["rates"]["EUR"]
        return f"💵 دلار (USD → IRR): {usd_to_irr:,.0f} ریال\n💶 یورو (EUR → USD): {usd_to_eur:.2f}"
    except:
        return "❌ خطا در دریافت نرخ ارز"

# دریافت قیمت طلا از tgju.org
def get_gold():
    try:
        url = "https://www.tgju.org/gold"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        price = soup.find("td", {"data-market-row": "geram18"}).text.strip()
        return f"🥇 قیمت طلای ۱۸ عیار: {price}"
    except:
        return "❌ خطا در دریافت قیمت طلا"

# زمان و تاریخ شمسی
def get_time_date():
    tz = pytz.timezone("Asia/Tehran")
    now = jdatetime.datetime.now(tz)
    return f"⏰ ساعت: {now.strftime('%H:%M:%S')}\n📅 تاریخ: {now.strftime('%Y/%m/%d')}"

# منوی اصلی
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("💵 دلار و یورو", callback_data="currency")],
        [InlineKeyboardButton("🥇 قیمت طلا", callback_data="gold")],
        [InlineKeyboardButton("⏰ زمان و تاریخ", callback_data="time")],
        [InlineKeyboardButton("ℹ️ درباره ما", callback_data="about")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("به ربات اقتصادی خوش اومدی 🌍\nیکی از گزینه‌ها رو انتخاب کن:", reply_markup=reply_markup)

# مدیریت دکمه‌ها
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
        query.edit_message_text("👨‍💻 برنامه‌نویس: علی اصغر درویش پور\n🤖 ربات اقتصادی با قیمت لحظه‌ای دلار، یورو و طلا")

# اجرای ربات
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()    
