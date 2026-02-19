"""Command handlers for bot execution capabilities."""

import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.services.executor import run_shell, list_project_files, read_file

logger = logging.getLogger(__name__)


async def run_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /run <command> — execute a shell command on the local machine."""
    if not context.args:
        await update.message.reply_text(
            "Usage: `/run <command>`\n"
            "Example: `/run dir`",
            parse_mode="Markdown",
        )
        return

    command = " ".join(context.args)
    logger.info("Executing: %s", command)

    await update.message.reply_text(f"⏳ Running: `{command}`", parse_mode="Markdown")
    result = run_shell(command)

    try:
        await update.message.reply_text(result, parse_mode="Markdown")
    except Exception:
        await update.message.reply_text(result)


async def ls_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /ls [path] — list project files."""
    path = " ".join(context.args) if context.args else "."
    result = list_project_files(path)

    try:
        await update.message.reply_text(result, parse_mode="Markdown")
    except Exception:
        await update.message.reply_text(result)


async def cat_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /cat <filepath> — read a file."""
    if not context.args:
        await update.message.reply_text(
            "Usage: `/cat <filepath>`\n"
            "Example: `/cat bot/config.py`",
            parse_mode="Markdown",
        )
        return

    filepath = " ".join(context.args)
    result = read_file(filepath)

    try:
        await update.message.reply_text(result, parse_mode="Markdown")
    except Exception:
        await update.message.reply_text(result)
