import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import filetype
import os

# ---------------- تنظیمات لاگ ----------------
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ---------------- توکن ربات ----------------
TOKEN = os.getenv("BOT_TOKEN")  # یا مستقیم توکن بذار: "123456:ABC-DEF..."

# ---------------- دستورات ربات ----------------
def start(update, context):
    update.message.reply_text("سلام! من آنلاین هستم 🤖")

def help_command(update, context):
    update.message.reply_text("لیست دستورات:\n/start - شروع\n/help - کمک")

def handle_message(update, context):
    text = update.message.text
    update.message.reply_text(f"شما گفتید: {text}")

def handle_photo(update, context):
    photo_file = update.message.photo[-1].get_file()
    file_path = "photo.jpg"
    photo_file.download(file_path)

    kind = filetype.guess(file_path)
    if kind is not None:
        update.message.reply_text(f"📸 فرمت عکس: {kind.mime}")
    else:
        update.message.reply_text("فرمت ناشناخته است.")

# ---------------- اجرای اصلی ----------------
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # دستورات
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))

    # پیام متنی
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # عکس
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))

    # شروع
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
