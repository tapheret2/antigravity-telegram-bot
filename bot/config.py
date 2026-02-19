"""Configuration management — loads settings from .env file."""

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Immutable application settings loaded from environment."""

    telegram_token: str
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

        return cls(
            telegram_token=token,
            log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
        )


# Singleton
settings = Settings.from_env()
