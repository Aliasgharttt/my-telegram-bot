import os
import random
import pytz
import jdatetime
from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# گرفتن توکن از Environment
TOKEN = os.getenv("TOKEN")

# ساعت تهران
def get_tehran_time():
    tz = pytz.timezone("Asia/Tehran")
    now = datetime.now(tz)
    return now.strftime("%H:%M:%S")

# تاریخ شمسی
def get_shamsi_date():
    return jdatetime.date.today().strftime("%Y/%m/%d")

# جوک‌ها
jokes = [
    "یه روز یه مرد به ربات گفت: برو ظرفارو بشور... ربات گفت: من باتم نه مایع ظرفشویی! 🤖",
    "می‌دونی فرق آدم خجالتی با لپ‌تاپ چیه؟ لپ‌تاپ همیشه راحت روشن میشه 😅",
    "میگن پول خوشبختی نمیاره، درسته... ولی تاکسی اینترنتی رو مجانی میاره؟ 😂",
]

# منوی اصلی
def main_menu():
    keyboard = [
        [InlineKeyboardButton("🕒 ساعت تهران", callback_data="time")],
        [InlineKeyboardButton("📅 تاریخ شمسی", callback_data="date")],
        [InlineKeyboardButton("🎲 تاس", callback_data="dice")],
        [InlineKeyboardButton("😂 جوک", callback_data="joke")],
        [InlineKeyboardButton("👨‍💻 معرفی برنامه‌نویس", callback_data="dev")]
    ]
    return InlineKeyboardMarkup(keyboard)

# دکمه برگشت
def back_button():
    keyboard = [[InlineKeyboardButton("🔙 بازگشت", callback_data="back")]]
    return InlineKeyboardMarkup(keyboard)

# شروع
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("به ربات خوش اومدی 👋", reply_markup=main_menu())

# هندل دکمه‌ها
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "time":
        await query.edit_message_text(f"⏰ ساعت تهران: {get_tehran_time()}", reply_markup=back_button())
    elif query.data == "date":
        await query.edit_message_text(f"📅 تاریخ شمسی: {get_shamsi_date()}", reply_markup=back_button())
    elif query.data == "dice":
        await query.edit_message_text(f"🎲 عدد تاس: {random.randint(1,6)}", reply_markup=back_button())
    elif query.data == "joke":
        await query.edit_message_text(f"😂 {random.choice(jokes)}", reply_markup=back_button())
    elif query.data == "dev":
        await query.edit_message_text("👨‍💻 برنامه‌نویس: علی اصغر درویش پور", reply_markup=back_button())
    elif query.data == "back":
        await query.edit_message_text("منوی اصلی 👇", reply_markup=main_menu())

# اجرای ربات
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    port = int(os.environ.get("PORT", 8443))
    app.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path=TOKEN,
        webhook_url=f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}"
    )

if __name__ == "__main__":
    main()
