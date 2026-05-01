Agentic Finance Studio 🚀

Institutional Sentiment → Actionable Crypto Signals

Agentic Finance Studio is an AI-powered Telegram bot that helps traders turn market sentiment into clear, actionable insights.

Instead of reacting to noise, the bot delivers structured intelligence for assets like BTC and XRP, combining sentiment data, price tracking, and smart alerts.

🎯 Project Vision

Retail traders often struggle with:

- Information overload
- Late entries
- Lack of clear signals

Agentic Finance Studio solves this by combining:

1. Institutional Sentiment
   Data from SoSoValue (when available)

2. Market Data Intelligence
   Multi-source pricing (SoSoValue → CoinGecko → Binance)

3. Actionable Alerts
   Simple insights delivered via Telegram in real-time
   
🛠️ Tech Stack

- Backend: Python (Async)
- Bot Framework: python-telegram-bot
- Hosting: JustRunMy.App
- APIs:
  - SoSoValue (primary)
  - CoinGecko (fallback)
  - Binance (backup)
- Security:
  - Environment variables ("TELEGRAM_TOKEN", "SOSO_API_KEY")
  - No hardcoded credentials

🚀 Features

- 📊 Live Price Tracking
  BTC, ETH, XRP, SOL via simple commands

- 🔁 Multi-API Fallback System
  Ensures price data is always available

- 🐳 Whale Alerts (MVP)
  XRP/BTC movement detection (expandable)

- ⚡ Fast Telegram Interface
  Clean and instant responses

📦 Installation

git clone https://github.com/your-username/agentic-finance-studio.git
cd agentic-finance-studio
pip install -r requirements.txt

🔐 Environment Variables

Set these in your hosting platform or ".env" file:

TELEGRAM_TOKEN=your_telegram_bot_token
SOSO_API_KEY=your_sosovalue_api_key

▶️ Run the Bot

python main.py

💬 Telegram Commands

/start        - Show menu
/test         - Check bot status
/btc          - Bitcoin price
/eth          - Ethereum price
/xrp          - XRP price
/sol          - Solana price
/price <sym>  - Custom coin
/whale        - Whale alert (MVP)

📈 Roadmap

✅ Wave 1 — MVP

- Telegram bot live
- Multi-API pricing
- Basic whale alerts

🚧 Wave 2 — Intelligence

- Real sentiment scoring
- Trade signals (Entry, TP, SL)

🔮 Wave 3 — Execution

- SoDEX integration
- One-click trades
- Automated alerts

⚠️ Disclaimer

This project is for educational purposes only.
Not financial advice.

🤝 Links

- Telegram Bot: https://t.me/AgenticFinanceBot
- Developer: fxscalpersignals
- Buildathon: SoSoValue & SoDEX
