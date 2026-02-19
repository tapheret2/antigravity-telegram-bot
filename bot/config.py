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


def get_ollama_url() -> str:
    """Return Ollama server URL, default localhost:11434."""
    return os.getenv("OLLAMA_URL", "http://localhost:11434")


def get_ollama_model() -> str:
    """Return the Ollama model name to use."""
    return os.getenv("OLLAMA_MODEL", "llama3.2")


