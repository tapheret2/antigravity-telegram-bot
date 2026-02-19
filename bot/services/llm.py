"""Ollama LLM adapter — sends messages to local Ollama and returns responses."""

import logging
import httpx
from bot.config import get_ollama_url, get_ollama_model

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
