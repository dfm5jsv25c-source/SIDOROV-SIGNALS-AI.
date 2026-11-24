
import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)
from market import analyze_eurusd

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 SIDOROV SIGNALS AI\n\n"
        "Бот работает!\n"
        "💶 Пара: EUR/USD\n"
        "📊 Режим: DEMO\n\n"
        "Команды:\n"
        "/eurusd — получить справочный курс\n"
        "/help — помощь"
    )

async def eurusd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        result = analyze_eurusd()
        await update.message.reply_text(result)
    except Exception as error:
        logging.exception("Ошибка получения курса")
        await update.message.reply_text(
            "Не удалось получить курс. Попробуй позже."
        )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start — запуск\n"
        "/eurusd — курс EUR/USD\n"
        "/help — помощь"
    )

def main():
    token = os.environ["BOT_TOKEN"]
    port = int(os.environ.get("PORT", "10000"))
    base_url = os.environ["RENDER_EXTERNAL_URL"].rstrip("/")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("eurusd", eurusd))
    app.add_handler(CommandHandler("help", help_command))

    app.run_webhook(
        listen="0.0.0.0",
        port=port,
        url_path="telegram",
        webhook_url=f"{base_url}/telegram",
        drop_pending_updates=True
    )

if __name__ == "__main__":
    main()

