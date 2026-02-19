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

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    level=settings.log_level,
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Command handlers
# ---------------------------------------------------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    await update.message.reply_text(
        "🚀 *Antigravity Bot is online.*\n\n"
        "I'm your mobile work brain.\n"
        "I can chat, execute commands, and manage files on your machine.\n\n"
        "Type /help to see all commands.",
        parse_mode="Markdown",
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command."""
    await update.message.reply_text(
        "*Antigravity Bot — Commands*\n\n"
        "💬 *Chat:* Just send a message\n"
        "🔧 `/run <cmd>` — Run a shell command\n"
        "📂 `/ls [path]` — List project files\n"
        "📄 `/cat <file>` — Read a file\n"
        "🤖 `/mode` — Show LLM config\n"
        "❓ `/help` — This help\n\n"
        "*Work modes* (auto-detected):\n"
        "💡 Brainstorm · 📋 Plan · ✍️ Draft · 🔍 Review · ⚖️ Decide",
        parse_mode="Markdown",
    )


async def mode_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /mode — show current LLM config."""
    await update.message.reply_text(
        "🤖 *LLM:* Gemini 2.0 Flash\n"
        "🔗 *Provider:* Google AI",
        parse_mode="Markdown",
    )

# ---------------------------------------------------------------------------
# Error handler
# ---------------------------------------------------------------------------

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors and notify the user."""
    logger.error("Unhandled exception:", exc_info=context.error)

    if isinstance(update, Update) and update.message:
        await update.message.reply_text(
            "⚠️ Something went wrong. Please try again."
        )

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    """Build and run the bot in polling mode."""
    app = ApplicationBuilder().token(settings.telegram_token).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("mode", mode_cmd))
    app.add_handler(CommandHandler("run", run_cmd))
    app.add_handler(CommandHandler("ls", ls_cmd))
    app.add_handler(CommandHandler("cat", cat_cmd))

    # Message router
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, route_message))

    # Global error handler
    app.add_error_handler(error_handler)

    logger.info("Bot started — LLM: Gemini 2.0 Flash")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
