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
    """Route incoming text message through Gemini with detected work mode."""
    from bot.services.llm import ask_gemini
    from telegram.constants import ChatAction

    text = update.message.text
    mode = detect_mode(text)
    emoji = EMOJI_MAP.get(mode, "📩")

    logger.info("Mode detected: %s for message: %.50s", mode, text)

    # Show typing indicator while LLM processes
    await update.message.chat.send_action(ChatAction.TYPING)

    reply = await ask_gemini(text, mode)

    header = f"{emoji} *{mode.capitalize()}*\n\n" if mode != "general" else ""
    await update.message.reply_text(
        f"{header}{reply}",
        parse_mode="Markdown",
    )

