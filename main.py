from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "8785963267:AAGVuuqKNPb90TnRABoi6kLCVCnjqXQq2hM"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("START COMMAND RECEIVED")  # 👈 console check
    await update.message.reply_text("✅ Bot working perfectly!")

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))

print("Bot started...")
app.run_polling()
