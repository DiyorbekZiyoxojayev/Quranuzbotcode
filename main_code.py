import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from aiohttp import web
from telegram import InputFile
import io

BOT_TOKEN = os.getenv("8572236792:AAGiSeJwVdDc20pg7fK6J2PgtDvGh0QSXiA")
WEBHOOK_URL = os.getenv("https://cozy-manifestation.up.railway.app/8572236792:AAGiSeJwVdDc20pg7fK6J2PgtDvGh0QSXiA
")

if not BOT_TOKEN or not WEBHOOK_URL:
    raise ValueError("BOT_TOKEN yoki WEBHOOK_URL o‘rnatilmagan!")

ARAB = "ara-quranindopak"
UZB = "uzb-muhammadsodik"

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
        audio_url = f"https://cdn.islamic.network/quran/audio/128/ar.alafasy/{audio_id}.mp3"
        audio_content = requests.get(audio_url).content

        msg = (
            f"📖 *Sura {sura}, Oyat {oyat_raqam}*\n\n"
            f"🕌 *Arabcha:*\n{arab_text}\n\n"
            f"🇺🇿 *O‘zbekcha:*\n{uzb_text}"
        )

        await update.message.reply_text(msg, parse_mode="Markdown")
        await update.message.reply_audio(audio=InputFile(io.BytesIO(audio_content), filename=f"{audio_id}.mp3"))

    except Exception as e:
        print("Xatolik:", e)
        await update.message.reply_text("❌ Format: /oyat 2 255")


app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("oyat", oyat))

async def handle(request):
    data = await request.json()
    update = Update.de_json(data, app.bot)
    await app.update_queue.put_nowait(update)
    return web.Response(text="ok")

async def on_startup(app_web):
    print("Webhook sozlanmoqda...")
    await app.bot.set_webhook(WEBHOOK_URL)

web_app = web.Application()
web_app.router.add_post(f"/{BOT_TOKEN}", handle)
web_app.on_startup.append(on_startup)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    web.run_app(web_app, host="0.0.0.0", port=port)
