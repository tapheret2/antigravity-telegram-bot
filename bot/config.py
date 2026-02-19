"""Configuration management — loads settings from .env file."""

import os
from dotenv import load_dotenv

load_dotenv()


def get_token() -> str:
    """Return the Telegram bot token or raise if missing."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token or token == "your-telegram-bot-token-here":
        raise ValueError(
            "TELEGRAM_BOT_TOKEN is not set. "
            "Copy .env.example to .env and add your token."
        )
    return token


def get_log_level() -> str:
    """Return configured log level, default INFO."""
    return os.getenv("LOG_LEVEL", "INFO").upper()


def get_gemini_key() -> str:
    """Return the Gemini API key or raise if missing."""
    key = os.getenv("GEMINI_API_KEY")
    if not key or key == "your-gemini-api-key-here":
        raise ValueError(
            "GEMINI_API_KEY is not set. "
            "Add it to your .env file."
        )
    return key

