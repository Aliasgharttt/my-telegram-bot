from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from config import Token   # توکن از config.py ایمپورت میشه

# دستور start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام 👋 ربات روشنه!")

# تابع اصلی
def main():
    app = Application.builder().token(Token).build()
    app.add_handler(CommandHandler("start", start))

    print("ربات شروع به کار کرد ✅")
    app.run_polling()

if __name__ == "__main__":
    main()
