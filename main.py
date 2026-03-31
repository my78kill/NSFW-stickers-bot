import os
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
from nudenet import NudeDetector
import tempfile

BOT_TOKEN = "8785963267:AAGVuuqKNPb90TnRABoi6kLCVCnjqXQq2hM"

detector = NudeDetector()

# 🟢 START COMMAND (test ke liye)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is running & ready to filter NSFW content!")

# 🟢 GROUP JOIN MESSAGE
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        if member.id == context.bot.id:
            await update.message.reply_text(
                "🤖 NSFW Filter Bot Activated!\n\n"
                "🚫 NSFW content will be automatically removed."
            )

# 🔥 NSFW CHECK
def is_nsfw(file_path):
    try:
        result = detector.detect(file_path)

        for item in result:
            if item['class'] in [
                'EXPOSED_BREAST_F',
                'EXPOSED_GENITALIA_F',
                'EXPOSED_GENITALIA_M',
                'EXPOSED_ANUS'
            ] and item['score'] > 0.6:
                return True

    except Exception as e:
        print("Detection error:", e)

    return False

# 📩 MAIN HANDLER
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message

    try:
        if msg.photo:
            file = await msg.photo[-1].get_file()

            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                await file.download_to_drive(tmp.name)

                if is_nsfw(tmp.name):
                    await msg.delete()

        elif msg.sticker:
            file = await msg.sticker.get_file()

            with tempfile.NamedTemporaryFile(delete=False, suffix=".webp") as tmp:
                await file.download_to_drive(tmp.name)

                if is_nsfw(tmp.name):
                    await msg.delete()

        elif msg.animation or msg.video:
            await msg.delete()

    except Exception as e:
        print("Error:", e)

# 🤖 APP
app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
app.add_handler(MessageHandler(filters.ALL, handle))

print("Bot running with welcome message...")
app.run_polling()
