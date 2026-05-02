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
        "Live Crypto Intelligence Bot\n\n"
        "*Commands:*\n"
        "/btc /eth /xrp /sol\n"
        "/price <symbol>\n"
        "/signal\n"
        "/whale\n"
        "/test",
        parse_mode='Markdown'
    )

# 🧪 TEST
async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is running perfectly!")

# 🐳 WHALE ALERT (BTC + XRP)
async def whale_alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        msg = await update.message.reply_text("🐳 Scanning market activity...")

        btc = requests.get(
            "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd",
            timeout=10
        )
        xrp = requests.get(
            "https://api.coingecko.com/api/v3/simple/price?ids=ripple&vs_currencies=usd",
            timeout=10
        )

        if btc.status_code != 200 or xrp.status_code != 200:
            await msg.edit_text("❌ Failed to fetch market data.")
            return

        btc_price = float(btc.json()["bitcoin"]["usd"])
        xrp_price = float(xrp.json()["ripple"]["usd"])

        btc_signal = "📈 Bullish" if btc_price > 70000 else "📉 Bearish" if btc_price < 60000 else "🟡 Ranging"
        xrp_signal = "🚨 Accumulation" if xrp_price > 1.35 else "⚠️ Dumping" if xrp_price < 1.20 else "🟡 Stable"

        await msg.edit_text(
            f"🐳 *WHALE REPORT*\n\n"
            f"BTC: ${btc_price:,.0f} → {btc_signal}\n\n"
            f"XRP: ${xrp_price:.4f} → {xrp_signal}",
            parse_mode='Markdown'
        )

    except Exception as e:
        logging.error(e)
        await update.message.reply_text("⚠️ Whale check failed.")

# 📊 SIGNAL (NEW — IMPORTANT FOR BUILDATHON)
async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        msg = await update.message.reply_text("📡 Generating BTC signal...")

        r = requests.get(
            "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd",
            timeout=10
        )

        if r.status_code != 200:
            await msg.edit_text("❌ Failed to fetch data.")
            return

        price = float(r.json()["bitcoin"]["usd"])

        entry = price
        tp = price * 1.015
        sl = price * 0.985

        await msg.edit_text(
            f"📊 *BTC SIGNAL*\n\n"
            f"💰 Price: ${price:,.0f}\n"
            f"🎯 Entry: ${entry:,.0f}\n"
            f"🏆 TP: ${tp:,.0f}\n"
            f"🛑 SL: ${sl:,.0f}\n"
            f"📈 Bias: Bullish",
            parse_mode='Markdown'
        )

    except Exception as e:
        logging.error(e)
        await update.message.reply_text("⚠️ Signal error.")

# 🎯 FORMAT
def format_price(price):
    if price < 1:
        return f"{price:.6f}"
    elif price < 100:
        return f"{price:.2f}"
    return f"{price:,.0f}"

# 📈 PRICE ENGINE
async def get_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if context.args:
            symbol = context.args[0].lower()
        else:
            symbol = update.message.text.replace('/', '').lower()

        display = symbol.upper()
        msg = await update.message.reply_text(f"🔍 Fetching {display}...")

        # SoSo (Primary)
        if SOSO_API_KEY:
            try:
                url = f"https://openapi.sosovalue.com/openapi/v1/asset/market/current-price?symbol={display}"
                headers = {"Authorization": f"Bearer {SOSO_API_KEY}"}
                r = requests.get(url, headers=headers, timeout=10)

                if r.status_code == 200:
                    data = r.json()
                    if data.get("data"):
                        item = data["data"][0]
                        price = float(item["price"])
                        await msg.edit_text(f"📊 {display}\n💰 ${format_price(price)}\n🔌 SoSoValue")
                        return
            except:
                pass

        # CoinGecko
        try:
            cg = COINGECKO_IDS.get(symbol, symbol)
            r = requests.get(
                f"https://api.coingecko.com/api/v3/simple/price?ids={cg}&vs_currencies=usd",
                timeout=10
            )
            if r.status_code == 200:
                data = r.json()
                if cg in data:
                    price = data[cg]["usd"]
                    await msg.edit_text(f"📊 {display}\n💰 ${format_price(price)}\n🔗 CoinGecko")
                    return
        except:
            pass

        # Binance
        try:
            r = requests.get(
                f"https://api.binance.com/api/v3/ticker/price?symbol={display}USDT",
                timeout=10
            )
            if r.status_code == 200:
                price = float(r.json()["price"])
                await msg.edit_text(f"📊 {display}\n💰 ${format_price(price)}\n🔗 Binance")
                return
        except:
            pass

        await msg.edit_text(f"❌ Could not fetch {display}")

    except Exception as e:
        logging.error(e)
        await update.message.reply_text("⚠️ Error occurred.")

# 🧠 MAIN
if __name__ == "__main__":
    if not TOKEN:
        raise ValueError("❌ TELEGRAM_TOKEN not set!")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("test", test))
    app.add_handler(CommandHandler("whale", whale_alert))
    app.add_handler(CommandHandler("signal", signal))
    app.add_handler(CommandHandler("price", get_price))

    for coin in ["btc", "eth", "xrp", "sol"]:
        app.add_handler(CommandHandler(coin, get_price))

    print("🚀 Bot running...")
    app.run_polling(drop_pending_updates=True)
