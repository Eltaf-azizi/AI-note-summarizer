from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    backend: str = os.getenv("SUM_BACKEND", "openai")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    hf_model: str = os.getenv("HF_MODEL", "facebook/bart-large-cnn")

    # App-level constraints
    max_upload_mb: int = 16

settings = Settings()
