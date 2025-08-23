from dataclasses import dataclass
from typing import List
from .config import settings
from .utils import detect_lang, sha256, ensure_cache_dir, cache_read, cache_write, chunk_by_words
from .summarizer import get_backend

@dataclass
class SummaryParams:
    length: str = "short"   # short | medium | long
    tone: str = "neutral"   # neutral | concise | bullets
    backend: str = settings.backend

class Pipeline:
    def __init__(self):
        self._backends = {}

    def _backend(self, name: str):
        if name not in self._backends:
            self._backends[name] = get_backend(name)
        return self._backends[name]
