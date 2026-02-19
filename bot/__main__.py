"""Entry point — run with `python -m bot`."""

import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from bot.config import settings
from bot.handlers.router import route_message
from bot.handlers.commands import run_cmd, ls_cmd, cat_cmd

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    level=settings.log_level,
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "🚀 *Antigravity Bot is online.*\n\n"
        "Chat with me or use commands:\n"
        "🔧 `/run <cmd>` — Run shell command\n"
        "📂 `/ls` — List files\n"
        "📄 `/cat <file>` — Read file\n"
        "❓ `/help` — All commands",
        parse_mode="Markdown",
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "*Antigravity Bot*\n\n"
        "💬 Chat: just send a message\n"
        "🔧 `/run <cmd>` — Shell command\n"
        "📂 `/ls [path]` — List files\n"
        "📄 `/cat <file>` — Read file\n"
        "🤖 `/mode` — LLM info\n"
        "❓ `/help` — This help",
        parse_mode="Markdown",
    )


async def mode_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "🤖 *LLM:* Gemini 2.0 Flash\n🔗 *Provider:* Google AI",
        parse_mode="Markdown",
    )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Unhandled exception:", exc_info=context.error)
    if isinstance(update, Update) and update.message:
        await update.message.reply_text("⚠️ Something went wrong.")


def main() -> None:
    app = ApplicationBuilder().token(settings.telegram_token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("mode", mode_cmd))
    app.add_handler(CommandHandler("run", run_cmd))
    app.add_handler(CommandHandler("ls", ls_cmd))
    app.add_handler(CommandHandler("cat", cat_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, route_message))
    app.add_error_handler(error_handler)

    logger.info("Bot started — Gemini 2.0 Flash")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
