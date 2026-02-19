"""Entry point — run with `python -m bot`."""

import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from bot.config import get_token, get_log_level

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    level=get_log_level(),
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    await update.message.reply_text(
        "🚀 *Antigravity Bot is online.*\n\n"
        "I'm your mobile work brain.\n"
        "Send me a message — I'll auto-detect your work mode:\n"
        "💡 Brainstorm · 📋 Plan · ✍️ Draft · 🔍 Review · ⚖️ Decide",
        parse_mode="Markdown",
    )

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    """Build and run the bot in polling mode."""
    from telegram.ext import MessageHandler, filters
    from bot.handlers.router import route_message

    token = get_token()

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))

    # Route all text messages through the mode-detection router
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, route_message))

    logger.info("Bot started in polling mode. Press Ctrl+C to stop.")
    app.run_polling()


if __name__ == "__main__":
    main()
