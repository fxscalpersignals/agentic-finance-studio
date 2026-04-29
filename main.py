import os
import requests
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# Setup Logging
logging.basicConfig(level=logging.INFO)

# Keys from Vault
TOKEN = os.getenv('TELEGRAM_TOKEN')
SOSO_API_KEY = os.getenv('SOSO_API_KEY')

# --- NEW: THE DATA FETCHER ---
def get_xrp_sentiment():
    url = "https://api.sosovalue.com/v1/asset/sentiment" # Target endpoint
    headers = {"Authorization": f"Bearer {SOSO_API_KEY}"}
    params = {"symbol": "XRP"}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        
        # We look for the "Sentiment Index" or "Inflow" in the response
        sentiment = data.get('data', {}).get('sentiment', 'No data')
        inflow = data.get('data', {}).get('inflow_24h', '0')
        
        return f"📊 XRP Analysis:\nSentiment: {sentiment}\n24h Inflow: {inflow}M"
    except Exception as e:
        return f"⚠️ Error fetching data: {str(e)}"

# --- COMMANDS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 Agentic Finance Studio is LIVE.\nUse /check to see XRP status.")

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_message = get_xrp_sentiment()
    await update.message.reply_text(status_message)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('check', check))
    application.run_polling()
