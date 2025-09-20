import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# گرفتن توکن از Environment Variables
TOKEN = os.getenv("BOT_TOKEN")

# دستور start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! 🎉 ربات با موفقیت ران شد 🚀")

# دستور help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("لیست دستورات:\n/start - شروع\n/help - راهنما")

# تابع اصلی
def main():
    if not TOKEN:
        raise ValueError("❌ BOT_TOKEN در Environment Variables ست نشده است.")

    # ساخت اپلیکیشن
    app = Application.builder().token(TOKEN).build()

    # ثبت هندلرها
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    # اجرای ربات
    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
