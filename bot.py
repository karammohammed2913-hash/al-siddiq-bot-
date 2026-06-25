from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
ApplicationBuilder,
CommandHandler,
MessageHandler,
CallbackQueryHandler,
ContextTypes,
filters
)

import yt_dlp
import os
import uuid
import json

TOKEN = "8997713378:AAH4tL_oeKXT3r4O1rFuhjEp9q9uxi3He3I"

USERS_FILE = "users.json"

user_links = {}

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
