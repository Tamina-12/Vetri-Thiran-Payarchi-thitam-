from pathlib import Path
from dotenv import load_dotenv
import os


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env
load_dotenv(BASE_DIR / ".env")


class Settings:
    """
    Application configuration.
    """

    APP_NAME: str = os.getenv("APP_NAME", "LegalEase")

    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    GEMINI_MODEL: str = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.8-flash"
    )

    BACKEND_URL: str = os.getenv(
        "BACKEND_URL",
        "http://127.0.0.1:8000"
    )

    ALLOW_DEMO_MODE: bool = (
        os.getenv("ALLOW_DEMO_MODE", "true").lower() == "true"
    )

    MAX_GENERATION_TOKENS: int = int(
        os.getenv("MAX_GENERATION_TOKENS", "6000")
    )

    TEMPERATURE: float = float(
        os.getenv("TEMPERATURE", "0.4")
    )


settings = Settings()