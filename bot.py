from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

import yt_dlp
import os
import uuid
import json

TOKEN = "8997713378:AAH4tL_oeKXT3r4O1rFuhjEp9q9uxi3He3I"

USERS_FILE = "users.json"


def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            return set(json.load(f))
    except:
        return set()


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(list(users), f)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    users = load_users()
    users.add(user_id)
    save_users(users)

    await update.message.reply_text(
        f"👋 أهلاً بك في بوت الصدّيق\n\n"
        f"📥 أرسل رابط TikTok أو YouTube أو Instagram\n\n"
        f"• Facebook\n\n"
        f"𝕏 X (Twitter)\n\n"
        f"🤍 استخدم البوت فيما يرضي الله\n\n"
        f"👥 عدد مستخدمي البوت: {len(users)}"
    )


async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    await update.message.reply_text("⏳ جاري تحميل الفيديو...")

    unique_name = str(uuid.uuid4())

    ydl_opts = {
        "format": "best",
        "outtmpl": unique_name + ".%(ext)s"
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

            ext = info["ext"]
            filename = f"{unique_name}.{ext}"

        with open(filename, "rb") as video:
            await update.message.reply_video(video)

        os.remove(filename)

    except Exception as e:
        print("ERROR:", e)
        await update.message.reply_text(
            "❌ حدث خطأ أثناء التحميل.\nتأكد من صحة الرابط ثم حاول مرة أخرى."
        )


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        download_video
    )
)

print("Bot is running...")

app.run_polling(drop_pending_updates=True)
