import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Grab keys from Environment Variables
TOKEN = os.environ.get("TELEGRAM_TOKEN")
SOSO_API_KEY = os.environ.get("SOSO_API_KEY")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Agentic Finance Studio is LIVE on fps.ms! Use /check for BTC data.")

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://api.sosovalue.xyz/v1/asset/market/current-price?symbol=BTC"
    headers = {"Authorization": SOSO_API_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        # Navigate the JSON structure to get the price
        price_data = data.get('data', [])
        if price_data:
            price = price_data[0].get('price', 'N/A')
            await update.message.reply_text(f"📊 BTC Current Price: ${price}")
        else:
            await update.message.reply_text("⚠️ Data received, but price is missing.")
    except Exception as e:
        await update.message.reply_text("❌ Connection error. Check your SOSO_API_KEY.")

if __name__ == "__main__":
    if not TOKEN:
        print("Error: TELEGRAM_TOKEN not found!")
    else:
        print("Bot is starting...")
        app = ApplicationBuilder().token(TOKEN).build()
        
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("check", check))
        
        app.run_polling()
