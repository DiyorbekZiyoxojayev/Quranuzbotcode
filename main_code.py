


import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("8572236792:AAGiSeJwVdDc20pg7fK6J2PgtDvGh0QSXiA")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable o‘rnatilmagan!")
ARAB = "ara-quranindopak"
UZB = "uzb-muhammadsodik"
QORI = "ar.alafasy"

def format_number(n):
    return str(n).zfill(3)

async def oyat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        
        sura = int(context.args[0])
        oyat_raqam = int(context.args[1])

       
        arab_url = f"https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions/{ARAB}/{sura}/{oyat_raqam}.json"
        uzb_url = f"https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions/{UZB}/{sura}/{oyat_raqam}.json"

        arab_text = requests.get(arab_url).json()["text"]
        uzb_text = requests.get(uzb_url).json()["text"]

      
        audio_id = f"{format_number(sura)}{format_number(oyat_raqam)}"
        audio_url = f"https://cdn.islamic.network/quran/audio/128/{QORI}/{audio_id}.mp3"

        msg = (
            f"📖 *Sura {sura}, Oyat {oyat_raqam}*\n\n"
            f"🕌 *Arabcha:*\n{arab_text}\n\n"
            f"🇺🇿 *O‘zbekcha:*\n{uzb_text}"
        )

      
        await update.message.reply_text(msg, parse_mode="Markdown")
        
        await update.message.reply_audio(audio_url)

    except Exception as e:
        print("Xatolik:", e)
        await update.message.reply_text("❌ Format: /oyat 2 255")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("oyat", oyat))
    print("Bot ishga tushdi...")
    app.run_polling()

