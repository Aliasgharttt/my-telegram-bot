import telebot
from telebot import types
import requests
from datetime import datetime
import pytz
import jdatetime

# خواندن توکن از فایل
with open("token.txt", "r") as f:
    TOKEN = f.read().strip()

bot = telebot.TeleBot(TOKEN)

# لیست جوک‌ها
jokes = [
    "رفتی نونوایی میگی نون داغ داری؟ میگه نه نون خودمونه 😂",
    "یکی از گوسفندا به چوپان گفت: چرا ما همیشه باید علف بخوریم؟ چوپان گفت: چون پیتزا گرونه 🤣",
    "میگن خوابیدن کار تنبلاست… پس من قهرمانم! 😴",
    "یه نفر از دکتر پرسید: دکتر چطور لاغر شم؟ دکتر گفت: کمتر بخور بیشتر بدو… اونم گفت: پس خدافظ، من نمیخوام! 😂",
]

# لیست جملات انگیزشی
quotes = [
    "هیچ وقت تسلیم نشو 💪",
    "تو قوی‌تر از چیزی هستی که فکر می‌کنی ✨",
    "هر روز یه شروع جدیده 🌱",
    "اگه می‌خوای به چیزی برسی، باید براش بجنگی 🔥",
]

# دریافت قیمت از API
def get_price(symbol):
    try:
        url = f"https://api.exchangerate.host/latest?base=USD"
        data = requests.get(url).json()
        if symbol == "USD":
            return "دلار آمریکا: ۱ دلار = {:.2f} تومان".format(data["rates"]["IRR"])
        elif symbol == "EUR":
            return "یورو: ۱ یورو = {:.2f} تومان".format(data["rates"]["IRR"] / data["rates"]["EUR"])
        elif symbol == "GOLD":
            # API رایگان طلا نداریم، به صورت تستی
            return "💰 قیمت طلا: حدودی ۲,۳۰۰,۰۰۰ تومان در هر گرم"
    except:
        return "❌ خطا در دریافت قیمت"

# /start
@bot.message_handler(commands=["start"])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📅 تاریخ شمسی", callback_data="date"))
    markup.add(types.InlineKeyboardButton("⏰ ساعت تهران", callback_data="time"))
    markup.add(types.InlineKeyboardButton("💵 دلار", callback_data="usd"))
    markup.add(types.InlineKeyboardButton("💶 یورو", callback_data="eur"))
    markup.add(types.InlineKeyboardButton("🪙 طلا", callback_data="gold"))
    markup.add(types.InlineKeyboardButton("🎲 تاس", callback_data="dice"))
    markup.add(types.InlineKeyboardButton("😂 جوک", callback_data="joke"))
    markup.add(types.InlineKeyboardButton("💡 انگیزشی", callback_data="quote"))
    markup.add(types.InlineKeyboardButton("👨‍💻 درباره برنامه‌نویس", callback_data="about"))
    bot.send_message(message.chat.id, "سلام 👋 به ربات خوش آمدی!\nاز منوی زیر یکی رو انتخاب کن:", reply_markup=markup)

# مدیریت دکمه‌ها
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "date":
        today = jdatetime.date.today()
        bot.send_message(call.message.chat.id, f"📅 تاریخ شمسی: {today}")
    elif call.data == "time":
        tz = pytz.timezone("Asia/Tehran")
        iran_time = datetime.now(tz).strftime("%H:%M:%S")
        bot.send_message(call.message.chat.id, f"⏰ ساعت تهران: {iran_time}")
    elif call.data == "usd":
        bot.send_message(call.message.chat.id, get_price("USD"))
    elif call.data == "eur":
        bot.send_message(call.message.chat.id, get_price("EUR"))
    elif call.data == "gold":
        bot.send_message(call.message.chat.id, get_price("GOLD"))
    elif call.data == "dice":
        bot.send_dice(call.message.chat.id)
    elif call.data == "joke":
        import random
        bot.send_message(call.message.chat.id, random.choice(jokes))
    elif call.data == "quote":
        import random
        bot.send_message(call.message.chat.id, random.choice(quotes))
    elif call.data == "about":
        bot.send_message(call.message.chat.id, "👨‍💻 برنامه‌نویس: علی اصغر درویش پور")

print("🤖 Bot is running...")
bot.infinity_polling()
