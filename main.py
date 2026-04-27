import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# Logging helps us see if the bot is actually receiving your clicks
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 Agentic Finance Studio is now ACTIVE.\n\n"
        "Connection Verified. Ready for SoSoValue API integration."
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ System Status: Online\n📡 Latency: Optimal")

if __name__ == '__main__':
    # Your verified API Token
    TOKEN = '8728186403:AAFnwOiAc6XL1L0T8U3wc1US9iWUkX28IaY'
    
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('status', status))
    
    print("Bot is starting...")
    application.run_polling()
