from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import requests
import os
import random

TOKEN = os.getenv("TOKEN")

# گرفتن قیمت دلار و یورو از چند API
def get_forex_price(symbol="USD"):
    urls = [
        "https://open.er-api.com/v6/latest/USD",
        "https://api.exchangerate.host/latest?base=USD",
    ]
    url = random.choice(urls)
    try:
        r = requests.get(url, timeout=5).json()
        if "rates" in r:
            return r["rates"].get(symbol)
    except:
        return None

# گرفتن قیمت طلا (انس جهانی و گرم 18)
def get_gold_price():
    try:
        r = requests.get("https://api.metals.live/v1/spot", timeout=5).json()
        # خروجی لیست هست: [{'gold': 1925.45}, ...]
        gold_usd = r[0].get("gold")
        if gold_usd:
            # هر انس ≈ 31.103 گرم → گرم 18 = 0.9 × (انس/31.103)
            gram18 = (gold_usd / 31.103) * 0.9
            return gold_usd, round(gram18, 2)
    except:
        return None, None

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💵 دلار", callback_data="usd"),
         InlineKeyboardButton("💶 یورو", callback_data="eur")],
        [InlineKeyboardButton("🥇 طلا", callback_data="gold")],
        [InlineKeyboardButton("🎲 تاس", callback_data="dice")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("سلام 👋 یکی از گزینه‌ها رو انتخاب کن:", reply_markup=reply_markup)

# دکمه‌ها
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "usd":
        price = get_forex_price("IRR")
        if price:
            text = f"💵 قیمت دلار به ریال: {price}"
        else:
            text = "❌ نتونستم قیمت دلار رو بگیرم"
        await query.edit_message_text(text=text)

    elif query.data == "eur":
        price = get_forex_price("EUR")
        if price:
            text = f"💶 قیمت یورو: {price}"
        else:
            text = "❌ نتونستم قیمت یورو رو بگیرم"
        await query.edit_message_text(text=text)

    elif query.data == "gold":
        gold_usd, gram18 = get_gold_price()
        if gold_usd:
            text = f"🥇 طلا:\nانس جهانی: {gold_usd} دلار\nگرم 18: {gram18} دلار"
        else:
            text = "❌ نتونستم قیمت طلا رو بگیرم"
        await query.edit_message_text(text=text)

    elif query.data == "dice":
        dice = random.randint(1, 6)
        await query.edit_message_text(text=f"🎲 تاس ریخته شد: {dice}")

# اجرای ربات
if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()
