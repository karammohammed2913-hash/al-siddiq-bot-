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

TOKEN = os.getenv("8997713378:AAH4tL_oeKXT3r4O1rFuhjEp9q9uxi3He3I")

USERS_FILE = "users.json"


def load_users():
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    except:
        return set()


def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(list(users), f)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    users = load_users()
    users.add(user_id)
    save_users(users)

    await update.message.reply_text(
        f"👋 أهلاً بك في بوت الصدّيق\n\n"
        f"📥 أرسل رابط فيديو من:\n"
        f"• YouTube\n"
        f"• YouTube Shorts\n"
        f"• TikTok\n"
        f"• Instagram\n"
        f"• Facebook\n\n"
        f"👥 عدد المستخدمين: {len(users)}"
    )


async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    await update.message.reply_text("⏳ جاري التحميل...")

    unique_name = str(uuid.uuid4())

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "outtmpl": unique_name + ".%(ext)s",
        "noplaylist": True,
        "quiet": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

            requested_file = ydl.prepare_filename(info)

            if not os.path.exists(requested_file):
                base = os.path.splitext(requested_file)[0]
                requested_file = base + ".mp4"

        file_size = os.path.getsize(requested_file)

        with open(requested_file, "rb") as media:

            if file_size < 49 * 1024 * 1024:
                await update.message.reply_video(
                    media,
                    caption="✅ تم التحميل بنجاح"
                )
            else:
                await update.message.reply_document(
                    media,
                    caption="✅ تم التحميل بنجاح"
                )

        os.remove(requested_file)

    except Exception as e:
        print("ERROR:", e)

        await update.message.reply_text(
            "❌ فشل تحميل الفيديو.\n"
            "تأكد أن الرابط صحيح ومتاح للعامة."
        )


def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN environment variable not found")

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


if __name__ == "__main__":
    main()
