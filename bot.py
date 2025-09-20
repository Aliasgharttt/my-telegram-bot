import logging
import requests
import pytz
from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler

# 🔹 توکن از فایل جدا
with open("token.txt") as f:
    TOKEN = f.read().strip()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# دکمه‌های شیشه‌ای
def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("📅 تاریخ شمسی", callback_data="date")],
        [InlineKeyboardButton("💰 قیمت دلار", callback_data="usd"),
         InlineKeyboardButton("💶 قیمت یورو", callback_data="eur")],
        [InlineKeyboardButton("🥇 قیمت طلا", callback_data="gold")],
        [InlineKeyboardButton("🎲 تاس", callback_data="dice"),
         InlineKeyboardButton("😂 جوک", callback_data="joke")]
    ]
    return InlineKeyboardMarkup(keyboard)

# شروع
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام 👋 من رباتت هستم!", reply_markup=get_main_keyboard())

# هندلر دکمه‌ها
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "date":
        now = datetime.now(pytz.timezone("Asia/Tehran"))
        await query.edit_message_text(f"📅 تاریخ امروز: {now.strftime('%Y/%m/%d %H:%M')}")

    elif query.data == "usd":
        price = get_price("usd")
        await query.edit_message_text(f"💵 دلار: {price} تومان")

    elif query.data == "eur":
        price = get_price("eur")
        await query.edit_message_text(f"💶 یورو: {price} تومان")

    elif query.data == "gold":
        price = get_price("gold")
        await query.edit_message_text(f"🥇 طلا: {price} تومان")

    elif query.data == "dice":
        from random import randint
        dice_num = randint(1, 6)
        await query.edit_message_text(f"🎲 عدد تاس: {dice_num}")

    elif query.data == "joke":
        joke = get_joke()
        await query.edit_message_text(f"😂 جوک:\n{joke}")

# تابع قیمت‌ها
def get_price(kind):
    try:
        # از یک API بازار ایران استفاده می‌کنیم
        url = "https://api.tgju.org/v1/market/summary/all"
        res = requests.get(url).json()
        if kind == "usd":
            return res["data"]["price_dollar_rl"]["p"]
        elif kind == "eur":
            return res["data"]["price_eur"]["p"]
        elif kind == "gold":
            return res["data"]["geram18"]["p"]
    except:
        return "❌ خطا در دریافت قیمت"

# تابع جوک ساده
def get_joke():
    jokes = [
        "رفتم دکتر گفت استراحت کن، گفتم نمی‌شه پروژه دیپلوی دارم! 😂",
        "می‌دونی فرق برنامه‌نویس با جادوگر چیه؟ هیچ‌کدوم کارشون درست کار نمی‌کنه ولی جادوگر باحال‌تره 🤣",
    ]
    from random import choice
    return choice(jokes)

# ران کردن بات
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__ == "__main__":
    main()
