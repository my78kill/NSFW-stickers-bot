import requests
import time
import hmac
import hashlib
import tempfile
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8785963267:AAGVuuqKNPb90TnRABoi6kLCVCnjqXQq2hM"

ACCESS_KEY = "HpW9bKMNBAvNk29y"
SECRET_KEY = "VHrSvfFltkDqTxR+j/uq+w=="

# 🔐 SIGNATURE GENERATE
def generate_headers():
    timestamp = str(int(time.time()))
    message = timestamp + ACCESS_KEY

    signature = hmac.new(
        SECRET_KEY.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()

    return {
        "Authorization": ACCESS_KEY,
        "x-hive-timestamp": timestamp,
        "x-hive-signature": signature
    }

# 🧠 NSFW CHECK
def is_nsfw(file_path):
    url = "https://api.thehive.ai/api/v2/task/sync"

    headers = generate_headers()

    files = {
        "media": open(file_path, "rb")
    }

    data = {
        "models": "nsfw"
    }

    try:
        response = requests.post(url, headers=headers, files=files, data=data)
        result = response.json()

        classes = result["status"][0]["response"]["output"][0]["classes"]

        for item in classes:
            if item["class"] == "nsfw" and item["score"] > 0.7:
                return True

    except Exception as e:
        print("Hive error:", e)

    return False

# 🟢 START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Hive NSFW Bot Active!")

# 🟢 WELCOME
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        if member.id == context.bot.id:
            await update.message.reply_text(
                "🤖 NSFW Filter Activated!\n🚫 Content monitored."
            )

# 📩 HANDLER
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg:
        return

    try:
        if msg.photo:
            file = await msg.photo[-1].get_file()

            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                await file.download_to_drive(tmp.name)

                if is_nsfw(tmp.name):
                    await msg.delete()

        elif msg.sticker:
            await msg.delete()

        elif msg.animation or msg.video:
            file = await msg.video.get_file() if msg.video else await msg.animation.get_file()

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
                await file.download_to_drive(tmp.name)

                if is_nsfw(tmp.name):
                    await msg.delete()

    except Exception as e:
        print("Error:", e)

# 🤖 APP
app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
app.add_handler(MessageHandler(filters.ALL, handle))

print("🚀 Hive Access+Secret Bot Running...")

app.run_polling(drop_pending_updates=True)
