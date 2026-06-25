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

TOKEN = "8997713378:AAE_25VY8NWL59Oe_Mish_MYVzOVCDPExFk"


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

app.run_polling(drop_pending_updates=True)users.add(user_id)
save_users(users)

await update.message.reply_text(
    f"👋 أهلاً بك في بوت الصدّيق\n\n"
    f"📥 أرسل رابط TikTok أو Instagram أو YouTube أو Facebook أو X\n\n"
    f"🤍 استخدم البوت فيما يرضي الله\n\n"
    f"👥 عدد مستخدمي البوت: {len(users)}"
)

async def receive_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
url = update.message.text.strip()

user_links[update.effective_user.id] = url

keyboard = [
    [
        InlineKeyboardButton("📱 360p", callback_data="360"),
        InlineKeyboardButton("📱 480p", callback_data="480")
    ],
    [
        InlineKeyboardButton("🎥 720p HD", callback_data="720")
    ],
    [
        InlineKeyboardButton("🎵 MP3", callback_data="mp3")
    ]
]

await update.message.reply_text(
    "🎥 اختر الجودة المطلوبة:",
    reply_markup=InlineKeyboardMarkup(keyboard)
)

async def quality_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
query = update.callback_query
await query.answer()

user_id = query.from_user.id

if user_id not in user_links:
    await query.message.reply_text("❌ أرسل الرابط مرة أخرى.")
    return

url = user_links[user_id]

await query.message.reply_text("⏳ جاري التحميل...")

unique_name = str(uuid.uuid4())

try:
    if query.data == "360":
        fmt = "best[height<=360]"
    elif query.data == "480":
        fmt = "best[height<=480]"
    elif query.data == "720":
        fmt = "best[height<=720]"
    else:
        fmt = "bestaudio"

    ydl_opts = {
        "format": fmt,
        "outtmpl": unique_name + ".%(ext)s"
    }

    if query.data == "mp3":
        ydl_opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192"
        }]

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

        if query.data == "mp3":
            filename = unique_name + ".mp3"
        else:
            ext = info["ext"]
            filename = f"{unique_name}.{ext}"

    if query.data == "mp3":
        with open(filename, "rb") as audio:
            await query.message.reply_audio(audio)
    else:
        with open(filename, "rb") as video:
            await query.message.reply_video(video)

    os.remove(filename)

except Exception as e:
    print("ERROR:", e)

    await query.message.reply_text(
        "❌ حدث خطأ أثناء التحميل."
    )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
MessageHandler(
filters.TEXT & ~filters.COMMAND,
receive_link
)
)

app.add_handler(
CallbackQueryHandler(quality_selected)
)

print("Bot is running...")

app.run_polling(drop_pending_updates=True)users.add(user_id)
save_users(users)

await update.message.reply_text(
    f"👋 أهلاً بك في بوت الصدّيق\n\n"
    f"📥 أرسل رابط TikTok أو Instagram أو YouTube أو Facebook أو X\n\n"
    f"🤍 استخدم البوت فيما يرضي الله\n\n"
    f"👥 عدد مستخدمي البوت: {len(users)}"
)

async def receive_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
url = update.message.text.strip()

user_links[update.effective_user.id] = url

keyboard = [
    [
        InlineKeyboardButton("📱 360p", callback_data="360"),
        InlineKeyboardButton("📱 480p", callback_data="480")
    ],
    [
        InlineKeyboardButton("🎥 720p HD", callback_data="720")
    ],
    [
        InlineKeyboardButton("🎵 MP3", callback_data="mp3")
    ]
]

await update.message.reply_text(
    "🎥 اختر الجودة المطلوبة:",
    reply_markup=InlineKeyboardMarkup(keyboard)
)

async def quality_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
query = update.callback_query
await query.answer()

user_id = query.from_user.id

if user_id not in user_links:
    await query.message.reply_text("❌ أرسل الرابط مرة أخرى.")
    return

url = user_links[user_id]

await query.message.reply_text("⏳ جاري التحميل...")

unique_name = str(uuid.uuid4())

try:

    if query.data == "360":
        fmt = "best[height<=360]"
    elif query.data == "480":
        fmt = "best[height<=480]"
    elif query.data == "720":
        fmt = "best[height<=720]"
    else:
        fmt = "bestaudio"

    ydl_opts = {
        "format": fmt,
        "outtmpl": unique_name + ".%(ext)s"
    }

    if query.data == "mp3":
        ydl_opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192"
        }]

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

        if query.data == "mp3":
            filename = unique_name + ".mp3"
        else:
            ext = info["ext"]
            filename = f"{unique_name}.{ext}"

    if query.data == "mp3":
        with open(filename, "rb") as audio:
            await query.message.reply_audio(audio)
    else:
        with open(filename, "rb") as video:
            await query.message.reply_video(video)

    os.remove(filename)

except Exception as e:
    print("ERROR:", e)

    await query.message.reply_text(
        "❌ حدث خطأ أثناء التحميل."
    )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
MessageHandler(
filters.TEXT & ~filters.COMMAND,
receive_link
)
)

app.add_handler(
CallbackQueryHandler(quality_selected)
)

print("Bot is running...")

app.run_polling(drop_pending_updates=True)
