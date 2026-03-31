import os
import tempfile
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from nudenet import NudeDetector

# 🔐 BOT TOKEN (hardcoded)
BOT_TOKEN = "8785963267:AAGVuuqKNPb90TnRABoi6kLCVCnjqXQq2hM"

print("🔄 Loading NudeNet model...")
detector = NudeDetector()
print("✅ Model loaded!")

# 🟢 START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📩 /start received")
    if update.message:
        await update.message.reply_text("✅ Bot is running & ready!")

# 🟢 WELCOME MESSAGE (group me add hone pe)
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("👥 New member update")
    for member in update.message.new_chat_members:
        if member.id == context.bot.id:
            await update.message.reply_text(
                "🤖 NSFW Filter Bot Activated!\n"
                "🚫 Adult content will be removed automatically."
            )

# 🔥 NSFW CHECK
def is_nsfw(file_path):
    try:
        results = detector.detect(file_path)

        for item in results:
            if item['class'] in [
                'EXPOSED_BREAST_F',
                'EXPOSED_GENITALIA_F',
                'EXPOSED_GENITALIA_M',
                'EXPOSED_ANUS'
            ] and item['score'] > 0.6:
                print("❌ NSFW detected:", item)
                return True

    except Exception as e:
        print("⚠️ Detection error:", e)

    return False

# 📩 MEDIA HANDLER
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message

    if not msg:
        return

    try:
        print("📥 Message received")

        # 📸 PHOTO
        if msg.photo:
            file = await msg.photo[-1].get_file()

            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                await file.download_to_drive(tmp.name)

                if is_nsfw(tmp.name):
                    await msg.delete()
                    print("🗑️ NSFW photo deleted")

        # 🎭 STICKER
        elif msg.sticker:
            file = await msg.sticker.get_file()

            with tempfile.NamedTemporaryFile(delete=False, suffix=".webp") as tmp:
                await file.download_to_drive(tmp.name)

                if is_nsfw(tmp.name):
                    await msg.delete()
                    print("🗑️ NSFW sticker deleted")

        # 🎞️ GIF / VIDEO
        elif msg.animation or msg.video:
            await msg.delete()
            print("🗑️ Animation/Video deleted")

    except Exception as e:
        print("⚠️ Handler error:", e)

# 🤖 APP SETUP
app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
app.add_handler(MessageHandler(filters.PHOTO | filters.STICKER | filters.VIDEO | filters.ANIMATION, handle))

print("🚀 Bot started...")

# 🔥 IMPORTANT FIX
app.run_polling(drop_pending_updates=True)
