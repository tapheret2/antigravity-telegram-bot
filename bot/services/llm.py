"""Ollama LLM adapter — sends messages to local Ollama and returns responses."""

import logging
import httpx
from bot.config import get_ollama_url, get_ollama_model

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


async def ask_llm(message: str, mode: str = "general") -> str:
    """Send a message to Ollama and return the text response.

    Args:
        message: The user's message text.
        mode: Detected work mode for system prompt selection.

    Returns:
        The LLM's text response.
    """
    system_prompt = SYSTEM_PROMPTS.get(mode, SYSTEM_PROMPTS["general"])
    url = f"{get_ollama_url()}/api/chat"
    model = get_ollama_model()

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message},
        ],
        "stream": False,
    }

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data["message"]["content"] or "⚠️ Empty response from Ollama."

    except httpx.TimeoutException:
        logger.error("Ollama request timed out")
        return "⚠️ Ollama timed out. Is the model loaded?"

    except Exception as e:
        logger.error("Ollama API error: %s", e)
        return f"⚠️ LLM error: {e}"
