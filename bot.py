from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import TOKEN   # خواندن توکن از فایل config.py

# دستور start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! 🌹 ربات با موفقیت فعاله.")

def main():
    # ساخت اپلیکیشن
    app = Application.builder().token(TOKEN).build()

    # ثبت دستور
    app.add_handler(CommandHandler("start", start))

    # اجرای بات
    app.run_polling()

if __name__ == "__main__":
    main()
