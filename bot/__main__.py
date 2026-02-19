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
        "Send me anything and I'll echo it back for now.",
        parse_mode="Markdown",
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo any text message back (placeholder for routing layer)."""
    await update.message.reply_text(f"📩 {update.message.text}")

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    """Build and run the bot in polling mode."""
    token = get_token()

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))

    # Catch-all echo — will be replaced by message router in Step 3
    from telegram.ext import MessageHandler, filters
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    logger.info("Bot started in polling mode. Press Ctrl+C to stop.")
    app.run_polling()


if __name__ == "__main__":
    main()
