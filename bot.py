import logging
import requests
import jdatetime
import pytz
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- خواندن توکن از فایل token.txt ---
try:
    with open("token.txt", "r") as f:
        TOKEN = f.read().strip()
        if not TOKEN:
            raise ValueError("❌ فایل token.txt خالی است!")
except FileNotFoundError:
    raise FileNotFoundError("❌ فایل token.txt پیدا نشد. مطمئن شو که کنار bot.py باشه.")

# فعال کردن لاگ برای دیباگ
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# دستور start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📅 تاریخ و ساعت", callback_data="time")],
        [InlineKeyboardButton("💵 قیمت دلار", callback_data="usd")],
        [InlineKeyboardButton("💶 قیمت یورو", callback_data="eur")],
        [InlineKeyboardButton("🪙 قیمت طلا", callback_data="gold")],
        [InlineKeyboardButton("😂 جوک", callback_data="joke")],
        [InlineKeyboardButton("🎲 تاس", callback_data="dice")],
        [InlineKeyboardButton("ℹ️ درباره", callback_data="about")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("سلام 👋 یک گزینه رو انتخاب کن:", reply_markup=reply_markup)

# هندلر دکمه‌ها
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "time":
        tehran_tz = pytz.timezone("Asia/Tehran")
        now = datetime.now(tehran_tz)
        jalali = jdatetime.datetime.fromgregorian(datetime=now).strftime("%Y/%m/%d %H:%M:%S")
        await query.edit_message_text(f"⏰ تاریخ و ساعت (ایران): {jalali}")

    elif query.data == "usd":
        try:
            response = requests.get("https://api.exchangerate.host/latest?base=USD")
            data = response.json()
            irr = data["rates"]["IRR"]
            await query.edit_message_text(f"💵 قیمت دلار:\n\n1 دلار = {irr:.0f} ریال")
        except:
            await query.edit_message_text("❌ خطا در دریافت قیمت دلار")

    elif query.data == "eur":
        try:
            response = requests.get("https://api.exchangerate.host/latest?base=EUR")
            data = response.json()
            irr = data["rates"]["IRR"]
            await query.edit_message_text(f"💶 قیمت یورو:\n\n1 یورو = {irr:.0f} ریال")
        except:
            await query.edit_message_text("❌ خطا در دریافت قیمت یورو")

    elif query.data == "gold":
        try:
            response = requests.get("https://www.metals-api.com/api/latest?access_key=demo&base=USD&symbols=XAU")
            data = response.json()
            gold_price = data["rates"]["XAU"]
            await query.edit_message_text(f"🪙 قیمت طلا (انس جهانی): {gold_price} دلار")
        except:
            await query.edit_message_text("❌ خطا در دریافت قیمت طلا")

    elif query.data == "joke":
        jokes = [
            "بهترین راه پولدار شدن تو ایران اینه که دلار نخری! 😂",
            "بهتره به جای رژیم گرفتن، اینترنت ایران استفاده کنی! چون همه چی قطع میشه. 🤣",
            "میگن خوشبختی با پول نمیاد، ولی خب با دلار ۵۰ تومنی خیلی راحت‌تر میاد! 😅"
        ]
        import random
        await query.edit_message_text(f"😂 جوک:\n\n{random.choice(jokes)}")

    elif query.data == "dice":
        import random
        await query.edit_message_text(f"🎲 عدد تاس: {random.randint(1,6)}")

    elif query.data == "about":
        await query.edit_message_text("👨‍💻 برنامه‌نویس: علی اصغر درویش پور")

# ران اصلی
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    print("✅ ربات روشن شد و در حال اجراست...")
    app.run_polling()

if __name__ == "__main__":
    main()
