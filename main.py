import os
import requests
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# 1. Setup Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 2. Get Secrets from GitHub Vault
TOKEN = os.getenv('TELEGRAM_TOKEN')
SOSO_API_KEY = os.getenv('SOSO_API_KEY')

# 3. Data Fetching Logic
def get_xrp_data():
    # Using the standard SoSoValue asset detail endpoint for stable data
    url = "https://api.sosovalue.com/v1/asset/detail" 
    headers = {"Authorization": f"Bearer {SOSO_API_KEY}"}
    params = {"symbol": "XRP"}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json().get('data', {})
            price = data.get('price', 'N/A')
            change = data.get('change_24h', '0')
            
            # Simple Whale logic: If 24h change is high, flag it
            whale_msg = ""
            if abs(float(change)) > 5:
                whale_msg = "\n🚨 VOLATILITY ALERT: Heavy movement detected!"
                
            return f"📊 XRP Status:\nPrice: ${price}\n24h Change: {change}%{whale_msg}"
        else:
            return f"❌ API Error: {response.status_code}. Check if API Key is valid."
    except Exception as e:
        return f"⚠️ Connection Error: {str(e)}"

# 4. Bot Commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 Agentic Finance Studio Active.\n"
        "Use /check to get live XRP data."
    )

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Fetching live data from SoSoValue...")
    result = get_xrp_data()
    await update.message.reply_text(result)

# 5. Run the Bot
if __name__ == '__main__':
    if not TOKEN or not SOSO_API_KEY:
        print("CRITICAL ERROR: Keys missing in GitHub Secrets!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler('start', start))
        app.add_handler(CommandHandler('check', check))
        
        print("Bot is starting... Press Ctrl+C to stop.")
        app.run_polling()
