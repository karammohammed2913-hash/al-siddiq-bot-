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

TOKEN = "8997713378:AAH4tL_oeKXT3r4O1rFuhjEp9q9uxi3He3I"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 أهلاً بيك في بوت الصدّيق\n\n"
        "📥 ابعت لينك TikTok أو YouTube أو Instagram"
    )


async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    await update.message.reply_text("⏳ جاري التحميل...")

    unique_name = str(uuid.uuid4())

    ydl_opts = {
        'format': 'best',
        'outtmpl': unique_name + '.%(ext)s'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

            ext = info['ext']
            filename = f"{unique_name}.{ext}"

        with open(filename, "rb") as video:
            await update.message.reply_video(video)

        os.remove(filename)

    except Exception as e:
        print(e)
        await update.message.reply_text("❌ حدث خطأ أثناء التحميل")


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
