
from langchain_openai import ChatOpenAI

from personal_agentic_assistant.core.config import settings


def get_llm() -> ChatOpenAI:
    if not settings.OLLAMA_API_KEY:
        raise ValueError(
            "OLLAMA_API_KEY is missing. "
            "Add your Ollama Cloud API key to .env"
        )

    return ChatOpenAI(
        model=settings.OLLAMA_MODEL,
        api_key=settings.OLLAMA_API_KEY,
        base_url=settings.OLLAMA_BASE_URL,
        temperature=0.7,
        timeout=60,
        max_retries=2,
    )
