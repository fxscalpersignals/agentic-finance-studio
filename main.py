import os
import requests
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 1. Grab keys from Back4app Environment Variables
TOKEN = os.environ.get("TELEGRAM_TOKEN")
SOSO_API_KEY = os.environ.get("SOSO_API_KEY")

# 2. Define the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Agentic Finance Studio is LIVE! Use /check for market data.")

# 3. Define the /check command
async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Using SoSoValue BTC price endpoint as an example
    url = "https://api.sosovalue.xyz/v1/asset/market/current-price?symbol=BTC"
    headers = {"Authorization": SOSO_API_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        price = data.get('data', [{}])[0].get('price', 'N/A')
        await update.message.reply_text(f"📊 BTC Current Price: ${price}")
    except Exception as e:
        await update.message.reply_text("❌ Connection error. Please check your API keys.")

# 4. The main block that runs the bot
if __name__ == "__main__":
    if not TOKEN:
        print("CRITICAL ERROR: TELEGRAM_TOKEN not found in environment!")
    else:
        print("Bot is waking up...")
        app = ApplicationBuilder().token(TOKEN).build()
        
        # Add the command handlers
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("check", check))
        
        # This keeps the bot running 24/7
        app.run_polling()
