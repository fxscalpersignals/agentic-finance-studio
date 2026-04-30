import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Load environment variables (Hidden from GitHub via .gitignore)
load_dotenv()

# Securely fetch keys from the server environment
TOKEN = os.getenv("TELEGRAM_TOKEN")
SOSO_API_KEY = os.getenv("SOSO_API_KEY")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Entry point for users."""
    await update.message.reply_text(
        "🚀 **Agentic Finance Studio Terminal**\n\n"
        "Professional Market Data Bot for SoSoValue Buildathon\n\n"
        "Commands:\n"
        "/btc - Bitcoin Price\n"
        "/xrp - Ripple Price\n"
        "/eth - Ethereum Price\n"
        "/price <symbol> - Check any coin (e.g., /price SOL)"
    )

async def get_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Fetches real-time price data from SoSoValue API."""
    # Check if the user provided a symbol after /price
    if context.args:
        symbol = context.args[0].upper()
    else:
        # Otherwise, use the command name itself (btc, xrp, eth)
        command = update.message.text.split()[0].replace('/', '')
        symbol = command.upper()

    url = f"https://api.sosovalue.xyz/v1/asset/market/current-price?symbol={symbol}"
    headers = {"Authorization": SOSO_API_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        price_data = data.get('data', [])
        
        if price_data:
            price = price_data[0].get('price', 'N/A')
            # Formatting price to look professional
            await update.message.reply_text(f"📊 **{symbol}** Price: `${price}`")
        else:
            await update.message.reply_text(f"⚠️ Symbol {symbol} not found on SoSoValue.")
    except Exception:
        await update.message.reply_text("❌ Connection error. Please try again later.")

if __name__ == "__main__":
    print("Agentic Finance Bot is starting...")
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Command Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("btc", get_price))
    app.add_handler(CommandHandler("xrp", get_price))
    app.add_handler(CommandHandler("eth", get_price))
    app.add_handler(CommandHandler("price", get_price))
    
    # Start the bot
    app.run_polling(drop_pending_updates=True)
