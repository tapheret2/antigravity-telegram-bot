"""Gemini LLM adapter — sends messages to Google Gemini and returns responses."""

import asyncio
import logging
from google import genai
from bot.config import get_gemini_key

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Core identity
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

SYSTEM_PROMPTS: dict[str, str] = {
    "brainstorm": IDENTITY + "MODE: Brainstorming.\nExpand ideas, suggest variations, explore angles.",
    "plan": IDENTITY + "MODE: Planning.\nBreak into numbered steps. Flag dependencies.",
    "draft": IDENTITY + "MODE: Drafting.\nProduce clean text ready for refinement.",
    "review": IDENTITY + "MODE: Reviewing.\nList issues, suggest fixes. Be constructive.",
    "decide": IDENTITY + "MODE: Decision support.\nCompare options with pros/cons. Recommend.",
    "general": IDENTITY + "MODE: General assistant.\nAnswer helpfully and concisely.",
}


async def ask_llm(message: str, mode: str = "general") -> str:
    """Send a message to Gemini and return the text response.

    Retries automatically on rate limit (429) errors.
    """
    system_prompt = SYSTEM_PROMPTS.get(mode, SYSTEM_PROMPTS["general"])
    max_retries = 3

    for attempt in range(max_retries):
        try:
            client = genai.Client(api_key=get_gemini_key())
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=message,
                config=genai.types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    max_output_tokens=2048,
                    temperature=0.7,
                ),
            )
            return response.text or "⚠️ Empty response."

        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                wait = (attempt + 1) * 15
                logger.warning("Rate limited (attempt %d/%d), retry in %ds", attempt + 1, max_retries, wait)
                if attempt < max_retries - 1:
                    await asyncio.sleep(wait)
                    continue
                return "⏳ Rate limit — đợi ~1 phút rồi thử lại."

            logger.error("Gemini error: %s", e)
            return "⚠️ Lỗi AI. Thử lại nhé."
