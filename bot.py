import os
import logging
import requests
from random import randint
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get('BOT_TOKEN')

# دریافت قیمت‌ها از TGJU (معتبرترین منبع)
def get_currency_price(currency):
    try:
        response = requests.get('https://api.tgju.org/v1/data/sana/json')
        data = response.json()
        
        if currency == 'usd':
            usd_price = data['sana']['data']['price']
            return f"💰 قیمت دلار: {usd_price:,} تومان"
        elif currency == 'eur':
            eur_price = data['sana']['data']['eur']['price']
            return f"💶 قیمت یورو: {eur_price:,} تومان"
    except Exception as e:
        return f"⚠️ خطا در دریافت قیمت: {str(e)}"

def get_gold_price():
    try:
        response = requests.get('https://api.tgju.org/v1/data/geram/json')
        data = response.json()
        gold_price = data['geram']['data']['price']
        return f"🥇 قیمت هر گرم طلای ۱۸ عیار: {gold_price:,} تومان"
    except Exception as e:
        return f"⚠️ خطا در دریافت قیمت طلا: {str(e)}"

# منوی اصلی
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💰 قیمت دلار", callback_data='usd')],
        [InlineKeyboardButton("💶 قیمت یورو", callback_data='eur')],
        [InlineKeyboardButton("🥇 قیمت طلا", callback_data='gold')],
        [InlineKeyboardButton("🎲 تاس بازی", callback_data='dice')],
        [InlineKeyboardButton("👨‍💻 معرفی برنامه نویس", callback_data='developer')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        '🤖 به ربات قیمت‌گیر من خوش آمدید!\n\n'
        '📊 قیمت‌های لحظه‌ای از معتبرترین منابع\n'
        'لطفاً یکی از گزینه‌ها را انتخاب کنید:',
        reply_markup=reply_markup
    )

# هندلر دکمه‌ها
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'usd':
        message = get_currency_price('usd')
    elif query.data == 'eur':
        message = get_currency_price('eur')
    elif query.data == 'gold':
        message = get_gold_price()
    elif query.data == 'dice':
        dice_value = randint(1, 6)
        message = f"🎲 تاس شما: {dice_value}"
    elif query.data == 'developer':
        message = "👨‍💻 برنامه نویس: علی اصغر درویش پور\n📧 Email: example@email.com"
    else:
        message = "دستور نامعتبر!"
    
    await query.edit_message_text(text=message)

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.run_polling()

if __name__ == '__main__':
    main()
