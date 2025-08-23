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

    def summarize(self, text: str, params: SummaryParams):
        text = text.strip()
        if not text:
            raise ValueError("No text provided")

        key = sha256(text + f"|{params.length}|{params.tone}|{params.backend}")
        ensure_cache_dir()
        cached = cache_read(key)
        if cached:
            cached["from_cache"] = True
            return cached

        lang = detect_lang(text)
        backend = self._backend(params.backend)

        chunks = chunk_by_words(text, target_words=280)
        partials: List[str] = []
        for ch in chunks:
            partials.append(backend.summarize(ch, params.length, params.tone, lang))

        joined = "\n\n".join(partials)
        final = backend.summarize(
            (
                "You will receive multiple partial summaries. Merge them into a single, coherent summary "
                "without duplicating points. Maintain factual accuracy.\n\nPartial summaries:\n" + joined
            ),
            params.length,
            params.tone,
            lang,
        )

        result = {
            "summary": final,
            "partials": partials,
            "language": lang,
            "backend": params.backend,
            "length": params.length,
            "tone": params.tone,
            "from_cache": False,
            "stats": {
                "num_chunks": len(chunks),
                "input_words": len(text.split()),
            },
        }
        cache_write(key, result)
        return result
