import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")
APP_URL = os.getenv("APP_URL")  # آدرس سرویس روی Render

# === توابع گرفتن قیمت‌ها ===
def get_price(currency):
    try:
        if currency == "dollar":
            url = "https://api.exchangerate.host/latest?base=USD&symbols=IRR"
            data = requests.get(url).json()
            return f"💵 دلار: {round(data['rates']['IRR'])} ریال"

        elif currency == "euro":
            url = "https://api.exchangerate.host/latest?base=EUR&symbols=IRR"
            data = requests.get(url).json()
            return f"💶 یورو: {round(data['rates']['IRR'])} ریال"

        elif currency == "gold":
            # این API نمونه است، می‌تونی عوض کنی
            url = "https://api.metals.live/v1/spot"
            data = requests.get(url).json()
            price = data[0]['gold']
            return f"🥇 طلا (انس جهانی): {price} دلار"

    except:
        return "❌ خطا در دریافت قیمت"

# === منو اصلی ===
def main_menu():
    keyboard = [
        [InlineKeyboardButton("💵 دلار", callback_data="dollar"),
         InlineKeyboardButton("💶 یورو", callback_data="euro")],
        [InlineKeyboardButton("🥇 طلا", callback_data="gold"),
         InlineKeyboardButton("🎲 تاس", callback_data="dice")],
        [InlineKeyboardButton("👨‍💻 معرفی برنامه‌نویس", callback_data="about")],
    ]
    return InlineKeyboardMarkup(keyboard)

def back_menu():
    keyboard = [[InlineKeyboardButton("🔙 بازگشت", callback_data="back")]]
    return InlineKeyboardMarkup(keyboard)

# === دستور /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام 👋 به ربات خوش اومدی!", reply_markup=main_menu())

# === مدیریت دکمه‌ها ===
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data in ["dollar", "euro", "gold"]:
        text = get_price(query.data)
        await query.edit_message_text(text, reply_markup=back_menu())

    elif query.data == "dice":
        from random import randint
        await query.edit_message_text(f"🎲 عدد شما: {randint(1,6)}", reply_markup=back_menu())

    elif query.data == "about":
        await query.edit_message_text("👨‍💻 برنامه‌نویس: [اسم شما یا لینک تماس]", reply_markup=back_menu())

    elif query.data == "back":
        await query.edit_message_text("منو اصلی:", reply_markup=main_menu())

# === اجرای ربات با وبهوک ===
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.getenv("PORT", 8443)),
        url_path=TOKEN,
        webhook_url=f"{APP_URL}/{TOKEN}"
    )

if __name__ == "__main__":
    main()
