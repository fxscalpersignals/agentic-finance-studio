import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 1. Get the keys we saved in Back4app
TOKEN = os.environ.get("TELEGRAM_TOKEN")
SOSO_API_KEY = os.environ.get("SOSO_API_KEY")

# 2. Define the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am your Finance Bot. Use /check to get market data.")

# 3. Define the /check command (using SoSoValue API)
async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://api.sosovalue.xyz/v1/asset/market/current-price?symbol=BTC"
    headers = {"Authorization": SOSO_API_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        price = data.get('data', [{}])[0].get('price', 'N/A')
        await update.message.reply_text(f"Current BTC Price: ${price}")
    except Exception as e:
        await update.message.reply_text("Error fetching data. Check your API key!")

# 4. The main engine that keeps the bot alive
if __name__ == "__main__":
    if not TOKEN:
        print("Error: TELEGRAM_TOKEN not found!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("check", check))
        
        print("Bot is waking up...")
        app.run_polling()
