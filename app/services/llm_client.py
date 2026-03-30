from typing import Optional
from groq import Groq

from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


client: Optional[Groq] = None

if settings.GROQ_API_KEY:
    try:
        client = Groq(api_key=settings.GROQ_API_KEY)
    except Exception as e:
        logger.error(f"Failed to initialize Groq client: {e}")
        client = None
else:
    logger.warning("GROQ_API_KEY missing → LLM disabled")


# LLM CALL FUNCTION

def call_llm(system_prompt: str, user_prompt: str) -> str:
    """
    Calls Groq LLaMA API safely
    """

    if client is None:
        logger.warning("LLM client unavailable → returning empty response")
        return ""

    try:
        response = client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.MAX_TOKENS,
        )

        content = response.choices[0].message.content

        if not content:
            return ""

        return content.strip()

    except Exception as e:
        logger.error(f"LLM call failed: {str(e)}")
        return ""