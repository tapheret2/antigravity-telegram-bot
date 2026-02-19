"""Gemini LLM adapter — sends messages to Google Gemini and returns responses."""

import logging
from google import genai
from bot.config import get_gemini_key

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Core identity (shared across all modes)
# ---------------------------------------------------------------------------
IDENTITY = (
    "You are Antigravity, a Telegram-based mobile work assistant. "
    "You help your user think, plan, decide, write, and build incrementally. "
    "The user is a developer who often works away from their computer, "
    "using Telegram as a low-friction workspace for REAL work.\n\n"
    "RULES:\n"
    "- Be concise. Prefer bullet points and numbered steps.\n"
    "- No chit-chat. You are a focused work tool.\n"
    "- If something is complex, split into parts.\n"
    "- Optimize for momentum, not perfection.\n"
    "- Tone: professional, calm, direct.\n"
    "- The user can use /run, /ls, /cat commands to execute actions on their machine.\n"
    "- When the user asks you to DO something (create files, run commands), "
    "tell them the exact /run or command to use, don't just give instructions.\n"
)

# ---------------------------------------------------------------------------
# System prompt per work mode
# ---------------------------------------------------------------------------
SYSTEM_PROMPTS: dict[str, str] = {
    "brainstorm": (
        IDENTITY +
        "MODE: Brainstorming.\n"
        "Expand the user's ideas, suggest variations, explore angles. "
        "Use bullet points. Push thinking further."
    ),
    "plan": (
        IDENTITY +
        "MODE: Planning.\n"
        "Break things into numbered steps. Estimate effort if relevant. "
        "Flag dependencies. Keep it actionable."
    ),
    "draft": (
        IDENTITY +
        "MODE: Drafting.\n"
        "Produce clean, polished text ready for refinement. "
        "Match the user's tone. Output the draft directly."
    ),
    "review": (
        IDENTITY +
        "MODE: Reviewing.\n"
        "List issues and suggest fixes. Highlight what's good. "
        "Be direct and constructive."
    ),
    "decide": (
        IDENTITY +
        "MODE: Decision support.\n"
        "Compare options with pros/cons. Give a clear recommendation "
        "and justify it briefly."
    ),
    "general": (
        IDENTITY +
        "MODE: General assistant.\n"
        "Answer the user's question helpfully and concisely."
    ),
}


def _get_client() -> genai.Client:
    """Create and return a Gemini client."""
    return genai.Client(api_key=get_gemini_key())


async def ask_llm(message: str, mode: str = "general") -> str:
    """Send a message to Gemini and return the text response.

    Args:
        message: The user's message text.
        mode: Detected work mode for system prompt selection.

    Returns:
        The LLM's text response.
    """
    system_prompt = SYSTEM_PROMPTS.get(mode, SYSTEM_PROMPTS["general"])

    try:
        client = _get_client()
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=message,
            config=genai.types.GenerateContentConfig(
                system_instruction=system_prompt,
                max_output_tokens=2048,
                temperature=0.7,
            ),
        )
        return response.text or "⚠️ Empty response from Gemini."

    except Exception as e:
        logger.error("Gemini API error: %s", e)
        return f"⚠️ LLM error: {e}"
