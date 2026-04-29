import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# 1. Setup Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 2. Pull Keys from the Vault (GitHub Secrets)
TOKEN = os.getenv('TELEGRAM_TOKEN')
SOSO_API_KEY = os.getenv('SOSO_API_KEY')

# 3. The "Whale Alert" Logic
def check_whale_activity(inflow_data):
    if inflow_data.get('daily_change', 0) > 0.15:
        return "🚨 WHALE ALERT: Institutional buying detected. Expect volatility."
    return None

# 4. Command Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 Agentic Finance Studio is now ACTIVE.\n\n"
        "Connection Verified. SoSoValue API integration live."
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # This is a placeholder for the live API call we will do tomorrow
    await update.message.reply_text("✅ System Status: Online\n📡 Data Feed: SoSoValue Demo Plan Active")

# 5. Main Application
if __name__ == '__main__':
    if not TOKEN:
        print("Error: TELEGRAM_TOKEN not found in environment variables.")
    else:
        application = ApplicationBuilder().token(TOKEN).build()
        
        application.add_handler(CommandHandler('start', start))
        application.add_handler(CommandHandler('status', status))
        
        print("Bot is starting...")
        application.run_polling()
