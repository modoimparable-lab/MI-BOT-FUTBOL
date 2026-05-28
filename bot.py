import os
import requests
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Usamos variables de entorno para mayor seguridad (configuradas en Render)
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
FOOTBALL_TOKEN = os.getenv('FOOTBALL_TOKEN')
HEADERS = { 'X-Auth-Token': FOOTBALL_TOKEN }

def obtener_equipo_match(liga_id, nombre_parcial):
    url = f'https://api.football-data.org/v4/competitions/{liga_id}/standings'
    try:
        data = requests.get(url, headers=HEADERS).json()
        for row in data['standings'][0]['table']:
            if nombre_parcial.lower() in row['team']['name'].lower():
                return row
    except:
        return None
    return None

async def analizar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 3:
        await update.message.reply_text("Uso: /analizar [LigaID] [Local] [Visitante]")
        return
    
    liga, local, visitante = context.args[0], context.args[1], context.args[2]
    stats_l = obtener_equipo_match(liga, local)
    stats_v = obtener_equipo_match(liga, visitante)
    
    if stats_l and stats_v:
        respuesta = f"?? *Análisis: {stats_l['team']['name']} vs {stats_v['team']['name']}*\n\n"
        respuesta += f"Puntos {stats_l['team']['shortName']}: {stats_l['points']}\n"
        respuesta += f"Puntos {stats_v['team']['shortName']}: {stats_v['points']}\n"
        respuesta += f"Goles Favor {stats_l['team']['shortName']}: {stats_l['goalsFor']}"
        await update.message.reply_text(respuesta, parse_mode='Markdown')
    else:
        await update.message.reply_text("No encontré los equipos, intenta con un nombre más corto.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("analizar", analizar))
    print("Bot activo...")
    app.run_polling()