from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "8785963267:AAGVuuqKNPb90TnRABoi6kLCVCnjqXQq2hM"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("START WORKING")
    await update.message.reply_text("✅ Bot is alive!")

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))

print("Bot running...")
app.run_polling(drop_pending_updates=True)
