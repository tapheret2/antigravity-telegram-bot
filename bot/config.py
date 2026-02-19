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
        if not token:
            raise ValueError("TELEGRAM_BOT_TOKEN is not set.")

        gemini_key = os.getenv("GEMINI_API_KEY", "")
        if not gemini_key:
            raise ValueError("GEMINI_API_KEY is not set.")

        return cls(
            telegram_token=token,
            gemini_api_key=gemini_key,
            log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
        )


# Singleton
settings = Settings.from_env()


def get_gemini_key() -> str:
    return settings.gemini_api_key
