import os
import telebot
from telebot import types
import random
from datetime import datetime
import jdatetime

# =========================
# دریافت توکن از متغیر محیطی
# =========================
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("❌ توکن پیدا نشد! مطمئن شو BOT_TOKEN رو تو Render ست کردی.")

bot = telebot.TeleBot(TOKEN)

# =========================
# منو اصلی (دکمه‌ها)
# =========================
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🃏 جوک جدید", "🎲 تاس")
    markup.add("🕒 ساعت و تاریخ", "ℹ️ درباره")
    return markup

# =========================
# شروع
# =========================
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "سلام! 👋\nبه ربات خوش اومدی.\nاز منو یکی رو انتخاب کن:",
        reply_markup=main_menu()
    )

# =========================
# جوک‌ها
# =========================
jokes = [
    "می‌دونی فرق تو با اینترنت چیه؟ اینترنت محدود داره ولی تو بی‌نهایت عزیزی! 😅",
    "معلم: چرا خوابیدی؟\nشاگرد: چون خواب بهترین درمان بی‌خوابی هست! 😂",
    "می‌دونی فرق موبایل با دوست چیه؟ موبایل همیشه شارژ می‌خواد ولی دوست شارژت می‌کنه! 😉",
    "یه روز یه کامپیوتر میره دکتر، دکتر میگه: مشکلت چیه؟ میگه: ویندوزم قفل کرده! 🤖",
    "فرق آدم موفق با ناموفق؟ آدم موفق سحرخیزه، ناموفق دکمه اسنوزو میزنه! ⏰😂",
]

@bot.message_handler(func=lambda m: m.text == "🃏 جوک جدید")
def send_joke(message):
    bot.send_message(message.chat.id, random.choice(jokes))

# =========================
# تاس
# =========================
@bot.message_handler(func=lambda m: m.text == "🎲 تاس")
def dice(message):
    bot.send_message(message.chat.id, f"🎲 عدد تاس: {random.randint(1,6)}")

# =========================
# ساعت و تاریخ
# =========================
@bot.message_handler(func=lambda m: m.text == "🕒 ساعت و تاریخ")
def datetime_now(message):
    now = datetime.now()
    jnow = jdatetime.datetime.now()
    text = (
        f"⏰ ساعت: {now.strftime('%H:%M:%S')}\n"
        f"📅 تاریخ میلادی: {now.strftime('%Y-%m-%d')}\n"
        f"📅 تاریخ شمسی: {jnow.strftime('%Y-%m-%d')}"
    )
    bot.send_message(message.chat.id, text)

# =========================
# درباره
# =========================
@bot.message_handler(func=lambda m: m.text == "ℹ️ درباره")
def about(message):
    bot.send_message(
        message.chat.id,
        "🤖 این ربات توسط *علی اصغر درویش پور* ساخته شده.\n\n"
        "🔹 قابلیت‌ها:\n"
        "🃏 جوک‌های بامزه\n"
        "🎲 تاس ریختن\n"
        "🕒 نمایش تاریخ و ساعت شمسی و میلادی\n"
        "✨ منوی شیشه‌ای زیبا",
        parse_mode="Markdown"
    )

# =========================
# fallback برای پیام‌های دیگه
# =========================
@bot.message_handler(func=lambda m: True)
def fallback(message):
    bot.send_message(message.chat.id, "از منو یکی رو انتخاب کن:", reply_markup=main_menu())

# =========================
# اجرای ربات
# =========================
bot.infinity_polling()
