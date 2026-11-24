
import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 SIDOROV SIGNALS AI\n\n"
        "Бот успешно запущен!\n"
        "📊 Режим: DEMO\n"
        "💱 Анализ: в разработке\n\n"
        "Реальные сигналы пока не подключены.\n"
        "Команда /help — помощь."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "SIDOROV SIGNALS AI\n\n"
        "/start — запуск\n"
        "/help — помощь\n\n"
        "Учебный режим. Сделки не открываются."
    )

def main():
    token = os.environ["BOT_TOKEN"]
    port = int(os.environ.get("PORT", "10000"))
    base_url = os.environ["RENDER_EXTERNAL_URL"].rstrip("/")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
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


