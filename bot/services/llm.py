"""Gemini LLM adapter — sends messages to Google Gemini and returns responses."""

import logging
from google import genai
from bot.config import get_gemini_key

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# System prompt per work mode
# ---------------------------------------------------------------------------
SYSTEM_PROMPTS: dict[str, str] = {
    "brainstorm": (
        "You are a creative brainstorming partner. Expand ideas, suggest "
        "variations, and push thinking further. Use bullet points. Be concise."
    ),
    "plan": (
        "You are a planning assistant. Break things into numbered steps, "
        "estimate effort, flag dependencies. Keep it actionable and short."
    ),
    "draft": (
        "You are a drafting assistant. Produce clean, polished text ready "
        "for refinement. Match the user's tone. Output the draft directly."
    ),
    "review": (
        "You are a code/document reviewer. List issues, suggest fixes, "
        "and highlight what's good. Be direct and constructive."
    ),
    "decide": (
        "You are a decision-support advisor. Compare options with pros/cons, "
        "give a clear recommendation, and justify it briefly."
    ),
    "general": (
        "You are Antigravity, a concise mobile work assistant on Telegram. "
        "Be helpful, professional, and brief. Use bullet points when possible."
    ),
}


def _get_client() -> genai.Client:
    """Create and return a Gemini client."""
    return genai.Client(api_key=get_gemini_key())


async def ask_gemini(message: str, mode: str = "general") -> str:
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
                max_output_tokens=1024,
                temperature=0.7,
            ),
        )
        return response.text or "⚠️ Empty response from Gemini."

    except Exception as e:
        logger.error("Gemini API error: %s", e)
        return f"⚠️ LLM error: {e}"
