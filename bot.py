import os
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

TOKEN = "8638132037:AAFIktnEveFj1oawLlgEkKV5UEYSWAYQDEk"

# Link qabul qilish
async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    if "youtube.com" not in url and "youtu.be" not in url:
        await update.message.reply_text("❌ YouTube link yubor.")
        return

    context.user_data["url"] = url

    keyboard = [
    [
        InlineKeyboardButton("360p", callback_data="360"),
        InlineKeyboardButton("720p", callback_data="720"),
        InlineKeyboardButton("1080p", callback_data="1080"),
    ],
    [
        InlineKeyboardButton("🎵 MP3", callback_data="mp3")
    ]
]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🎬 Video sifatini tanlang:",
        reply_markup=reply_markup
    )

# Sifat tanlanganda
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    choice = query.data          # 👈 SHU YO‘Q
    url = context.user_data.get("url")   # 👈 SHU HAM YO‘Q

    if choice == "mp3":
        await query.edit_message_text("🎵 MP3 yuklanmoqda...")

    ydl_opts = {
    "format": "bestaudio/best",
    "outtmpl": "audio.%(ext)s",
    "cookiefile": "/etc/secrets/cookies.txt",   # 🔥 SHUNI QO‘SH
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",
    }],
}

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Faylni avtomatik topish
        for file in os.listdir():
            if file.endswith(".mp3"):
                await query.message.reply_audio(audio=open(file, "rb"))
                os.remove(file)
                break

    except Exception as e:
        print("MP3 XATO:", e)

    return

    # Video qismi
    quality = choice
    await query.edit_message_text(f"⏳ {quality}p yuklanmoqda...")

    ydl_opts = {
    "format": f"best[height<={quality}]/best",
    "outtmpl": "video.%(ext)s",
    "merge_output_format": "mp4",
    "cookiefile": "/etc/secrets/cookies.txt",
}

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        await query.message.reply_video(video=open("video.mp4", "rb"))
        os.remove("video.mp4")

    except Exception:
        await query.message.reply_text("❌ Video yuklashda xatolik.")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
app.add_handler(CallbackQueryHandler(download_video))

print("Bot ishga tushdi 🚀")

import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import os

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

def run_web():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()

threading.Thread(target=run_web).start()

app.run_polling()

