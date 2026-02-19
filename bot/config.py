"""Configuration management — loads settings from .env file."""

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Immutable application settings loaded from environment."""

    telegram_token: str
    ollama_url: str
    ollama_model: str
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
            ollama_url=os.getenv("OLLAMA_URL", "http://localhost:11434"),
            ollama_model=os.getenv("OLLAMA_MODEL", "llama3.2"),
            log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
        )


# Singleton — created once at import time
settings = Settings.from_env()


# Convenience accessors (backward compat)
def get_token() -> str:
    return settings.telegram_token

def get_log_level() -> str:
    return settings.log_level

def get_ollama_url() -> str:
    return settings.ollama_url

def get_ollama_model() -> str:
    return settings.ollama_model
