import logging
import requests
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Telegram Bot Token - ab environment variable se lega
API_TOKEN = os.getenv("API_TOKEN")

# Hugging Face Model URL (free wala GPT-2)
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/gpt2"

logging.basicConfig(level=logging.INFO)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! I'm your AI Genie 🤖\nType anything and I'll reply with magic!"
    )

# Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    response = requests.post(
        HUGGINGFACE_API_URL,
        headers={"Authorization": f"Bearer "},  # Agar free model hai to blank raho
        json={"inputs": user_message}
    )
    if response.status_code == 200:
        data = response.json()
        generated_text = data[0]["generated_text"]
        await update.message.reply_text(generated_text)
    else:
        await update.message.reply_text("Sorry, AI server is busy. Try again later.")

def main():
    app = ApplicationBuilder().token(API_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
