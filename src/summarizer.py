from __future__ import annotations
import os
from typing import Optional
from .config import settings

# OpenAI SDK
try:
    from openai import OpenAI
except Exception:  # pragma: no cover
    OpenAI = None

# Local Transformers
try:
    from transformers import pipeline as hf_pipeline
except Exception:  # pragma: no cover
    hf_pipeline = None


class OpenAIBackend:
    def __init__(self, model: Optional[str] = None):
        if OpenAI is None:
            raise RuntimeError("openai package not available; install or use local backend")
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY missing; set it in .env")
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = model or settings.openai_model

    def summarize(self, text: str, length: str, tone: str, language_hint: Optional[str]):
        target = {
            "short": "3-5 concise sentences",
            "medium": "5-7 sentences, preserve key context",
            "long": "8-12 sentences with nuance",
        }.get(length, "3-5 concise sentences")
        style = {
            "neutral": "neutral, factual prose",
            "concise": "ultra-concise, remove fluff",
            "bullets": "return only bullet points (•), each on a new line",
        }.get(tone, "neutral, factual prose")

        sys = (
            "You are a careful, precise summarizer. Keep facts accurate, avoid hallucinations, "
            "and preserve crucial terms and numbers."
        )


def get_backend(name: str):
    if name == "openai":
        return OpenAIBackend()
    if name == "local":
        return LocalHFBackend()
    if name == "mock":
        return MockBackend()
    raise ValueError(f"Unknown backend: {name}")
