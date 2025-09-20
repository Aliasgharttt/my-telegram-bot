from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import TOKEN   # توکن از فایل config.py میاد

# دستور start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("سلام! ربات با موفقیت فعاله 🚀")

def main():
    # ساخت اپلیکیشن با توکن
    application = Application.builder().token(TOKEN).build()

    # اضافه کردن دستور start
    application.add_handler(CommandHandler("start", start))

    # اجرای ربات
    application.run_polling()

if __name__ == "__main__":
    main()
