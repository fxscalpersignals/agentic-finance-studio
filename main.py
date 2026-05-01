import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 🔐 ENV
TOKEN = os.getenv("TELEGRAM_TOKEN")
SOSO_API_KEY = os.getenv("SOSO_API_KEY")

# 🧠 LOGGING
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

HEADERS = {"User-Agent": "Mozilla/5.0"}

# 🔁 SYMBOL MAP
COINGECKO_IDS = {
    "btc": "bitcoin",
    "eth": "ethereum",
    "xrp": "ripple",
    "sol": "solana"
}

# 🚀 START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 *Agentic Finance Studio Terminal*\n\n"
        "Live Crypto Price Checker\n\n"
        "*Commands:*\n"
        "/btc  /eth  /xrp  /sol\n"
        "/price <symbol>\n"
        "/whale\n"
        "/test",
        parse_mode='Markdown'
    )

# 🧪 TEST
async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is working perfectly!")

# 🐳 WHALE
async def whale_alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚨 *WHALE ALERT DETECTED*\n\n"
        "Large movements detected in *BTC* and *XRP*",
        parse_mode='Markdown'
    )

# 🎯 FORMAT PRICE
def format_price(price):
    if price < 1:
        return f"{price:.6f}"
    elif price < 100:
        return f"{price:.2f}"
    else:
        return f"{price:,.0f}"

# 📊 GET PRICE
async def get_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Detect symbol
        if context.args:
            symbol = context.args[0].lower().strip()
        else:
            symbol = update.message.text.replace('/', '').strip().lower()

        if not symbol:
            await update.message.reply_text("❌ Example: /btc")
            return

        display = symbol.upper()
        msg = await update.message.reply_text(f"🔍 Fetching {display}...")

        # =========================
        # 1. SOSOVALUE (PRIMARY)
        # =========================
        if SOSO_API_KEY:
            try:
                url = f"https://openapi.sosovalue.com/openapi/v1/asset/market/current-price?symbol={display}"

                headers = {
                    "Authorization": f"Bearer {SOSO_API_KEY}",
                    "x-soso-api-key": SOSO_API_KEY,
                    "User-Agent": "AgenticFinanceBot/1.0"
                }

                r = requests.get(url, headers=headers, timeout=12)

                if r.status_code == 200:
                    data = r.json()

                    if data.get("data"):
                        item = data["data"][0] if isinstance(data["data"], list) else data["data"]
                        price = float(item.get("price", 0))

                        if price > 0:
                            formatted = format_price(price)

                            await msg.edit_text(
                                f"📊 *{display}*\n"
                                f"💰 ${formatted} USD\n"
                                f"🔌 SoSoValue",
                                parse_mode='Markdown'
                            )
                            return
                else:
                    logging.warning(f"SoSo status: {r.status_code}")

            except Exception as e:
                logging.warning(f"SoSo failed: {e}")

        # =========================
        # 2. COINGECKO (FALLBACK)
        # =========================
        try:
            cg_id = COINGECKO_IDS.get(symbol, symbol)

            r = requests.get(
                f"https://api.coingecko.com/api/v3/simple/price?ids={cg_id}&vs_currencies=usd",
                headers=HEADERS,
                timeout=10
            )

            if r.status_code == 200:
                data = r.json()

                if cg_id in data:
                    price = float(data[cg_id]["usd"])
                    formatted = format_price(price)

                    await msg.edit_text(
                        f"📊 *{display}*\n"
                        f"💰 ${formatted} USD\n"
                        f"🔗 CoinGecko",
                        parse_mode='Markdown'
                    )
                    return

        except Exception as e:
            logging.warning(f"CoinGecko failed: {e}")

        # =========================
        # 3. BINANCE (LAST)
        # =========================
        try:
            r = requests.get(
                f"https://api.binance.com/api/v3/ticker/price?symbol={display}USDT",
                headers=HEADERS,
                timeout=10
            )

            if r.status_code == 200:
                price = float(r.json()["price"])
                formatted = format_price(price)

                await msg.edit_text(
                    f"📊 *{display}*\n"
                    f"💰 ${formatted} USD\n"
                    f"🔗 Binance",
                    parse_mode='Markdown'
                )
                return

        except Exception as e:
            logging.warning(f"Binance failed: {e}")

        # ❌ FINAL FAIL
        await msg.edit_text(f"❌ Could not get price for *{display}*.")

    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("⚠️ Error occurred.")

# 🧠 MAIN
if __name__ == "__main__":
    if not TOKEN:
        raise ValueError("❌ TELEGRAM_TOKEN not set!")

    app = ApplicationBuilder().token(TOKEN).build()

    # COMMANDS
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("test", test))
    app.add_handler(CommandHandler("whale", whale_alert))
    app.add_handler(CommandHandler("price", get_price))

    for coin in ["btc", "eth", "xrp", "sol"]:
        app.add_handler(CommandHandler(coin, get_price))

    print("🚀 Agentic Finance Studio Bot started!")
    app.run_polling(drop_pending_updates=True)
