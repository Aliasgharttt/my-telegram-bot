import os
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# دریافت توکن از Environment
TOKEN = os.getenv("TOKEN")

# آدرس‌های API برای نرخ‌ها
DOLLAR_API = "https://api.exchangerate.host/latest?base=USD&symbols=IRR"
GOLD_API = "https://api.metals.live/v1/spot"

# تابع گرفتن قیمت دلار به تومان
def get_dollar_to_toman():
    try:
        r = requests.get(DOLLAR_API).json()
        rate = r["rates"]["IRR"] / 10  # چون ریال هست تقسیم بر 10 می‌کنیم
        return f"💵 قیمت دلار: {rate:,.0f} تومان"
    except:
        return "❌ خطا در دریافت قیمت دلار"

# تابع گرفتن قیمت طلا
def get_gold_to_toman():
    try:
        r = requests.get(GOLD_API).json()
        gold_price_usd = r[0][1]  # قیمت انس طلا به دلار
        # تقریبی: هر انس ≈ 31.1 گرم → قیمت هر گرم طلا
        gram_gold_usd = gold_price_usd / 31.1
        # دلار به تومان
        r_dollar = requests.get(DOLLAR_API).json()
        dollar_rate = r_dollar["rates"]["IRR"] / 10
        gram_gold_toman = gram_gold_usd * dollar_rate
        return f"🏅 قیمت طلا (هر گرم): {gram_gold_toman:,.0f} تومان"
    except:
        return "❌ خطا در دریافت قیمت طلا"

# منوی اصلی
def main_menu():
    keyboard = [
        [InlineKeyboardButton("💵 قیمت دلار", callback_data="dollar")],
        [InlineKeyboardButton("🏅 قیمت طلا", callback_data="gold")],
        [InlineKeyboardButton("👨‍💻 معرفی برنامه‌نویس", callback_data="dev")]
    ]
    return InlineKeyboardMarkup(keyboard)

# دستور start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام 👋\nیکی از گزینه‌های زیر رو انتخاب کن:", reply_markup=main_menu())

# هندلر دکمه‌ها
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "dollar":
        text = get_dollar_to_toman()
    elif query.data == "gold":
        text = get_gold_to_toman()
    elif query.data == "dev":
        text = "👨‍💻 برنامه‌نویس: [نام شما]\n📌 تماس: @YourUsername"
    else:
        text = "❌ گزینه نامعتبر"

    # اضافه کردن دکمه بازگشت
    keyboard = [
        [InlineKeyboardButton("🔙 بازگشت به منو", callback_data="back")]
    ]
    if query.data == "back":
        await query.edit_message_text("منوی اصلی:", reply_markup=main_menu())
    else:
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

# اجرای ربات
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    APP_URL = os.getenv("APP_URL")

    if APP_URL:
        app.run_webhook(
            listen="0.0.0.0",
            port=int(os.environ.get("PORT", 8443)),
            url_path=TOKEN,
            webhook_url=f"{APP_URL}/{TOKEN}"
        )
    else:
        app.run_polling()

if __name__ == "__main__":
    main()
