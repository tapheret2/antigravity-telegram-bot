"""Message routing — auto-detects work mode and dispatches accordingly."""

import logging
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Mode detection keywords
# ---------------------------------------------------------------------------
MODE_KEYWORDS: dict[str, list[str]] = {
    "brainstorm": ["brainstorm", "ideas", "explore", "what if", "possibilities"],
    "plan": ["plan", "steps", "roadmap", "timeline", "schedule", "how to"],
    "draft": ["draft", "write", "compose", "outline", "template"],
    "review": ["review", "check", "feedback", "issues", "fix"],
    "decide": ["decide", "compare", "choose", "option", "recommend", "pros cons"],
}

EMOJI_MAP: dict[str, str] = {
    "brainstorm": "💡",
    "plan": "📋",
    "draft": "✍️",
    "review": "🔍",
    "decide": "⚖️",
    "general": "📩",
}


def detect_mode(text: str) -> str:
    """Return detected work mode based on keyword matching."""
    lower = text.lower()
    for mode, keywords in MODE_KEYWORDS.items():
        if any(kw in lower for kw in keywords):
            return mode
    return "general"


async def route_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Route incoming text message based on detected work mode."""
    text = update.message.text
    mode = detect_mode(text)
    emoji = EMOJI_MAP.get(mode, "📩")

    logger.info("Mode detected: %s for message: %.50s", mode, text)

    # For now, acknowledge mode and echo.
    # Step 4 will wire this to the LLM adapter.
    if mode == "general":
        await update.message.reply_text(f"{emoji} {text}")
    else:
        await update.message.reply_text(
            f"{emoji} *Mode: {mode.capitalize()}*\n\n{text}",
            parse_mode="Markdown",
        )
