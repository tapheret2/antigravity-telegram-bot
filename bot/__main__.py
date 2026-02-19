"""Telegram ↔ IDE Bridge — file-based message relay.

The bot is a dumb pipe:
- User sends Telegram msg → saved to bridge/inbox/<timestamp>.json
- IDE (Claude) reads inbox, writes response to bridge/outbox/<timestamp>.txt
- Bot polls outbox, sends any new files to Telegram, then deletes them
"""

import asyncio
import json
import logging
import os
import time
from pathlib import Path
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from bot.config import settings
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
# Bridge directories
# ---------------------------------------------------------------------------
BRIDGE_DIR = Path(os.getcwd()) / "bridge"
INBOX_DIR = BRIDGE_DIR / "inbox"
OUTBOX_DIR = BRIDGE_DIR / "outbox"

INBOX_DIR.mkdir(parents=True, exist_ok=True)
OUTBOX_DIR.mkdir(parents=True, exist_ok=True)

# Store the chat_id so we know where to send outgoing messages
CHAT_ID_FILE = BRIDGE_DIR / "chat_id.txt"

# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start — register chat and show help."""
    # Save chat_id for outbox polling
    chat_id = update.message.chat_id
    CHAT_ID_FILE.write_text(str(chat_id))

    await update.message.reply_text(
        "🚀 *Antigravity Bridge is online.*\n\n"
        "Your messages go straight to Claude in the IDE.\n"
        "Responses come back here automatically.\n\n"
        "🔧 `/run <cmd>` — Run shell command\n"
        "📂 `/ls [path]` — List files\n"
        "📄 `/cat <file>` — Read file",
        parse_mode="Markdown",
    )
    logger.info("Chat registered: %s", chat_id)


async def relay_to_inbox(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Save incoming Telegram message to inbox as a JSON file."""
    # Save chat_id
    chat_id = update.message.chat_id
    CHAT_ID_FILE.write_text(str(chat_id))

    # Create inbox message file
    timestamp = int(time.time() * 1000)
    msg_file = INBOX_DIR / f"{timestamp}.json"

    msg_data = {
        "from": update.message.from_user.first_name,
        "text": update.message.text,
        "timestamp": update.message.date.isoformat(),
        "chat_id": chat_id,
    }

    msg_file.write_text(json.dumps(msg_data, ensure_ascii=False, indent=2))
    logger.info("Inbox: %s", update.message.text[:50])

    await update.message.reply_text("📨 Sent to Claude.")

# ---------------------------------------------------------------------------
# Outbox poller — checks for response files and sends them to Telegram
# ---------------------------------------------------------------------------

async def poll_outbox(app) -> None:
    """Background task: poll outbox dir and send any files to Telegram."""
    logger.info("Outbox poller started")

    while True:
        try:
            # Check for response files
            for f in sorted(OUTBOX_DIR.glob("*.txt")):
                text = f.read_text(encoding="utf-8").strip()
                if not text:
                    f.unlink()
                    continue

                # Get chat_id
                if not CHAT_ID_FILE.exists():
                    logger.warning("No chat_id registered yet, skipping")
                    break

                chat_id = int(CHAT_ID_FILE.read_text().strip())

                # Send to Telegram (split if >4096 chars)
                chunks = [text[i:i+4096] for i in range(0, len(text), 4096)]
                for chunk in chunks:
                    try:
                        await app.bot.send_message(
                            chat_id=chat_id,
                            text=chunk,
                            parse_mode="Markdown",
                        )
                    except Exception:
                        await app.bot.send_message(
                            chat_id=chat_id,
                            text=chunk,
                        )

                logger.info("Outbox sent: %s", f.name)
                f.unlink()  # Delete after sending

        except Exception as e:
            logger.error("Outbox poll error: %s", e)

        await asyncio.sleep(2)  # Poll every 2 seconds

# ---------------------------------------------------------------------------
# Error handler
# ---------------------------------------------------------------------------

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors and notify the user."""
    logger.error("Unhandled exception:", exc_info=context.error)
    if isinstance(update, Update) and update.message:
        await update.message.reply_text("⚠️ Something went wrong.")

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

async def post_init(app) -> None:
    """Start the outbox poller after the bot is initialized."""
    asyncio.create_task(poll_outbox(app))


def main() -> None:
    """Build and run the bridge bot."""
    app = ApplicationBuilder().token(settings.telegram_token).post_init(post_init).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("run", run_cmd))
    app.add_handler(CommandHandler("ls", ls_cmd))
    app.add_handler(CommandHandler("cat", cat_cmd))

    # All text messages → inbox
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, relay_to_inbox))

    # Error handler
    app.add_error_handler(error_handler)

    logger.info("Bridge started — inbox: %s, outbox: %s", INBOX_DIR, OUTBOX_DIR)
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
