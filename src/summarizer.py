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
        usr = (
            f"Summarize the following text in {target}. Style: {style}. "
            + (f"Language: {language_hint}. " if language_hint else "")
            + "Text:\n\n" + text
        )
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": sys}, {"role": "user", "content": usr}],
            temperature=0.2,
            max_tokens=700,
        )
        return resp.choices[0].message.content.strip()

class LocalHFBackend:
    def __init__(self, model: Optional[str] = None):
        if hf_pipeline is None:
            raise RuntimeError("transformers not installed; set SUM_BACKEND=openai or install transformers")
        self.pipe = hf_pipeline("summarization", model=(model or settings.hf_model))

    def summarize(self, text: str, length: str, tone: str, language_hint: Optional[str]):
        # Token/length guidance
        target = {
            "short": (50, 150),
            "medium": (120, 240),
            "long": (200, 360),
        }.get(length, (60, 160))
        out = self.pipe(text, min_length=target[0], max_length=target[1], do_sample=False)
        summary = out[0]["summary_text"].strip()
        if tone == "bullets":
            import re
            sents = re.split(r"(?<=[.!?])\s+", summary)
            sents = [s.strip() for s in sents if s.strip()]
            summary = "\n".join(f"• {s}" for s in sents)
        return summary


class MockBackend:
    """Deterministic backend for tests (no network)."""
    def summarize(self, text: str, length: str, tone: str, language_hint: Optional[str]):
        base = text.strip().split("\n")[0][:120]
        if tone == "bullets":
            return f"• {base}"
        return f"SUMMARY: {base}"
    

def get_backend(name: str):
    if name == "openai":
        return OpenAIBackend()
    if name == "local":
        return LocalHFBackend()
    if name == "mock":
        return MockBackend()
    raise ValueError(f"Unknown backend: {name}")
