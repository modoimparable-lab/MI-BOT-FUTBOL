import os
import requests
from telegram.ext import ApplicationBuilder, CommandHandler

TOKEN = os.getenv('TELEGRAM_TOKEN')

async def start(update, context):
    await update.message.reply_text("El bot esta activo y listo.")

if __name__ == '__main__':
    if not TOKEN:
        print("Error: TOKEN no configurado")
        exit(1)
        
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("Bot iniciado correctamente...")
    app.run_polling()
