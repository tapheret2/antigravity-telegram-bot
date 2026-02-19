"""Configuration management — loads settings from .env file."""

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Immutable application settings loaded from environment."""

    telegram_token: str
    gemini_api_key: str
    log_level: str

    @classmethod
    def from_env(cls) -> "Settings":
        """Create Settings from environment variables."""
        token = os.getenv("TELEGRAM_BOT_TOKEN", "")
        if not token or token == "your-telegram-bot-token-here":
            raise ValueError(
                "TELEGRAM_BOT_TOKEN is not set. "
                "Copy .env.example to .env and add your token."
            )

        gemini_key = os.getenv("GEMINI_API_KEY", "")
        if not gemini_key or gemini_key == "your-gemini-api-key-here":
            raise ValueError(
                "GEMINI_API_KEY is not set. "
                "Add it to your .env file."
            )

        return cls(
            telegram_token=token,
            gemini_api_key=gemini_key,
            log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
        )


# Singleton — created once at import time
settings = Settings.from_env()


# Convenience accessors
def get_token() -> str:
    return settings.telegram_token

def get_log_level() -> str:
    return settings.log_level

def get_gemini_key() -> str:
    return settings.gemini_api_key
