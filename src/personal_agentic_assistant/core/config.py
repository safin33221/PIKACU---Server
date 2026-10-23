
import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(PROJECT_ROOT / ".env")


class Settings:
    APP_NAME: str = "Pikacu"
    OLLAMA_API_KEY: str = os.getenv("OLLAMA_API_KEY", "")
    OLLAMA_BASE_URL: str = os.getenv(
        "OLLAMA_BASE_URL",
        "https://ollama.com/v1",
    )
    OLLAMA_MODEL: str = os.getenv(
        "OLLAMA_MODEL",
        "gemma4:31b",
    )


settings = Settings()
