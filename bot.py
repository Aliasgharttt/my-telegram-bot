# bot.py
import os
import telebot
from telebot import types
import random
from datetime import datetime
import jdatetime

# ====== بارگذاری توکن ======
# روش ایمن: توکن را در فایل token.txt قرار بده (یک خط، فقط توکن)
TOKEN = None
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or TOKEN

if not TOKEN:
    try:
        with open("token.txt", "r", encoding="utf-8") as f:
            TOKEN = f.read().strip()
    except FileNotFoundError:
        TOKEN = None

if not TOKEN:
    raise RuntimeError("توکن ربات پیدا نشد! فایل token.txt را بساز و توکن را داخل آن قرار بده (یا متغیر محیطی TELEGRAM_BOT_TOKEN را تنظیم کن).")

bot = telebot.TeleBot(TOKEN)

jokes = [
    "می‌دونی فرق تو با اینترنت چیه؟ اینترنت محدود داره ولی تو نه! 😂",
    "معلم: چرا مشق ننوشتی؟ دانش‌آموز: چون سگم خورد! معلم: راست یا دروغ؟ دانش‌آموز: راست، سگم خیلی گرسنه بود! 🤣",
    "یه نفر پرسید: چرا دیر اومدی؟ گفت: آلارم زنگ زد ولی خوابم برد! 😅",
    "دانشجو: استاد شب امتحان برنامه‌نویسی رو از کی شروع کنم؟ استاد: از الان! 😆",
    "پرسیدم «چرا همیشه پشت لپتاپ خندیدی؟» گفت: چون کدهاشو خوندم! 🤪",
    "یه روز برق رفت، شمع گفت: الان وقته درخشیدن! 🕯️",
    "طرف میره نانوایی میگه: ۵ دقیقه دیگه میام — الان ۵ ساله هنوز برنگشته! 😂",
    "داداشم میگه می‌خوام رژیم بگیرم... همون لحظه داشت پیتزا سفارش می‌داد! 🍕"
]

def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("⏰ زمان", callback_data="time"),
        types.InlineKeyboardButton("ℹ️ درباره", callback_data="about"),
    )
    markup.add(
        types.InlineKeyboardButton("😂 جوک", callback_data="joke"),
        types.InlineKeyboardButton("🎲 تاس", callback_data="dice"),
    )
    return markup

@bot.message_handler(commands=['start'])
def cmd_start(msg):
    bot.send_message(msg.chat.id, "سلام! 🎉\nربات من افتتاح شد.\nاز دکمه‌های زیر استفاده کن:", reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: True)
def on_inline(call):
    cid = call.message.chat.id
    if call.data == "time":
        iran_j = jdatetime.datetime.now()
        iran_g = datetime.now()
        text = f"📅 تاریخ شمسی: {iran_j.strftime('%Y/%m/%d')}\n⏰ ساعت: {iran_g.strftime('%H:%M:%S')}"
        bot.answer_callback_query(call.id)
        bot.send_message(cid, text)

    elif call.data == "about":
        bot.answer_callback_query(call.id)
        bot.send_message(cid, "👨‍💻 برنامه‌نویس: علی اصغر درویش پور\n📌 ساخته شده با Python و TeleBot")

    elif call.data == "joke":
        bot.answer_callback_query(call.id)
        bot.send_message(cid, random.choice(jokes))

    elif call.data == "dice":
        bot.answer_callback_query(call.id)
        num = random.randint(1,6)
        bot.send_message(cid, f"🎲 عدد تاس: {num}")

@bot.message_handler(commands=['joke'])
def cmd_joke(msg):
    bot.reply_to(msg, random.choice(jokes))

@bot.message_handler(commands=['time'])
def cmd_time(msg):
    iran_j = jdatetime.datetime.now()
    iran_g = datetime.now()
    bot.reply_to(msg, f"📅 تاریخ شمسی: {iran_j.strftime('%Y/%m/%d')}\n⏰ ساعت: {iran_g.strftime('%H:%M:%S')}")

if __name__ == "__main__":
    print("ربات روشن شد ✅")
    bot.infinity_polling()
