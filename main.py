import os
import requests
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- BACK4APP HEALTH CHECK TRICK ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is active")

def run_health_server():
    # Back4app looks for a response on port 8080
    server = HTTPServer(('0.0.0.0', 8080), HealthCheckHandler)
    server.serve_forever()

# Start the mini-webserver in a background thread
threading.Thread(target=run_health_server, daemon=True).start()
# ----------------------------------

# 1. Grab keys from Back4app Environment Variables
TOKEN = os.environ.get("TELEGRAM_TOKEN")
SOSO_API_KEY = os.environ.get("SOSO_API_KEY")

# 2. Define the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Agentic Finance Studio is LIVE! Use /check for market data.")

# 3. Define the /check command
async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://api.sosovalue.xyz/v1/asset/market/current-price?symbol=BTC"
    headers = {"Authorization": SOSO_API_KEY}
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        # Adjusted to match common API structures
        price_data = data.get('data', [])
        if price_data:
            price = price_data[0].get('price', 'N/A')
            await update.message.reply_text(f"📊 BTC Current Price: ${price}")
        else:
            await update.message.reply_text("⚠️ Data received, but price field is missing.")
    except Exception as e:
        await update.message.reply_text("❌ Connection error. Please check your API keys.")

# 4. The main block
if __name__ == "__main__":
    if not TOKEN:
        print("CRITICAL ERROR: TELEGRAM_TOKEN not found!")
    else:
        print("Bot is waking up...")
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("check", check))
        app.run_polling()
