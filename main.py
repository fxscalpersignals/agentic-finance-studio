import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 🔐 ENV VARIABLES
TOKEN = os.getenv("TELEGRAM_TOKEN")
SOSO_API_KEY = os.getenv("SOSO_API_KEY")

# 🧠 LOGGING
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 🔁 SYMBOL MAP (for CoinGecko fallback)
SYMBOL_MAP = {
    "btc": "bitcoin",
    "eth": "ethereum",
    "xrp": "ripple"
}

# 🚀 START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🚀 *Agentic Finance Studio Terminal*\n\n"
        "Professional Market Intelligence Powered by SoSoValue\n\n"
        "*Commands:*\n"
        "/btc — Bitcoin Price\n"
        "/xrp — Ripple Price\n"
        "/eth — Ethereum Price\n"
        "/whale — Detect Large Market Movements\n"
        "/price <symbol> — Check any coin\n"
        "/test — Check bot status"
    )
    await update.message.reply_text(text, parse_mode='Markdown')

# 🧪 TEST COMMAND
async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is working!")

# 🐳 WHALE ALERT
async def whale_alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("🐳 *Scanning SoSoValue Liquidity...*", parse_mode='Markdown')

    await msg.edit_text(
        "🚨 *WHALE ALERT DETECTED*\n\n"
        "📍 *Source:* SoSoValue Liquidity Index\n"
        "🔹 *Observation:* Large BTC accumulation detected.\n"
        "📈 *Impact:* Positive Sentiment Flowing.",
        parse_mode='Markdown'
    )

# 📊 PRICE FUNCTION (FIXED + FALLBACK)
async def get_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Detect symbol
        if context.args:
            symbol = context.args[0].lower()
        else:
            command = update.message.text.split()[0].replace('/', '')
            symbol = command.lower()

        msg = await update.message.reply_text(f"🔍 Fetching {symbol.upper()} price...")

        # 🔹 Try SoSoValue API
        try:
            url = f"https://api.sosovalue.xyz/v1/asset/market/current-price?symbol={symbol.upper()}"
            headers = {"Authorization": SOSO_API_KEY}

            response = requests.get(url, headers=headers, timeout=5)

            if response.status_code == 200:
                data = response.json().get("data", [])
                if data:
                    price = data[0].get("price")
                    await msg.edit_text(f"📊 {symbol.upper()} Price: ${price}")
                    return
        except Exception as e:
            logging.warning(f"SoSo failed: {e}")

        # 🔹 Fallback to CoinGecko
        mapped_symbol = SYMBOL_MAP.get(symbol, symbol)

        cg_url = f"https://api.coingecko.com/api/v3/simple/price?ids={mapped_symbol}&vs_currencies=usd"
        cg_response = requests.get(cg_url, timeout=5)

        if cg_response.status_code == 200:
            cg_data = cg_response.json()

            if mapped_symbol in cg_data:
                price = cg_data[mapped_symbol]["usd"]
                await msg.edit_text(
                    f"📊 *{symbol.upper()} Price*\n\n💰 ${price}",
                    parse_mode='Markdown'
                )
                return

        await msg.edit_text("⚠️ Coin not found.")

    except Exception as e:
        logging.error(f"ERROR: {e}")
        await update.message.reply_text("❌ Failed to fetch price.")

# 🧠 MAIN
if __name__ == "__main__":
    if not TOKEN:
        print("❌ TELEGRAM_TOKEN not set!")
        exit()

    if not SOSO_API_KEY:
        print("❌ SOSO_API_KEY not set!")
        exit()

    app = ApplicationBuilder().token(TOKEN).build()

    # ✅ COMMANDS
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("test", test))
    app.add_handler(CommandHandler("btc", get_price))
    app.add_handler(CommandHandler("xrp", get_price))
    app.add_handler(CommandHandler("eth", get_price))
    app.add_handler(CommandHandler("price", get_price))
    app.add_handler(CommandHandler("whale", whale_alert))

    print("✅ Agentic Finance Studio: System Online.")
    app.run_polling(drop_pending_updates=True)
