import hashlib
import os
from io import BytesIO
from typing import Optional
from langdetect import detect
from werkzeug.datastructures import FileStorage
from pypdf import PdfReader
from docx import Document

CACHE_DIR = "cache"

def ensure_cache_dir():
    os.makedirs(CACHE_DIR, exist_ok=True)

def sha256(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def cache_path(key: str) -> str:
    ensure_cache_dir()
    return os.path.join(CACHE_DIR, f"{key}.json")


def cache_read(key: str):
    import json
    path = cache_path(key)
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
    return None

def cache_write(key: str, obj: dict):
    import json
    path = cache_path(key)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)



def load_any(file: FileStorage) -> str:
    """Load text from txt, md, pdf, docx uploads."""
    filename = (file.filename or "").lower()
    data = file.read()

    if filename.endswith((".txt", ".md", ".markdown")):
        return data.decode("utf-8", errors="ignore")

    if filename.endswith(".pdf"):
        stream = BytesIO(data)
        reader = PdfReader(stream)
        pages = []
        for p in reader.pages:
            try:
                pages.append(p.extract_text() or "")
            except Exception:
                pages.append("")
        return "\n\n".join(pages)

    if filename.endswith(".docx"):
        stream = BytesIO(data)
        doc = Document(stream)
        return "\n".join(p.text for p in doc.paragraphs)

    raise ValueError("Unsupported file type. Use .txt, .md, .pdf, or .docx")


def detect_lang(text: str) -> Optional[str]:
    try:
        return detect(text)
    except Exception:
        return None


def chunk_by_words(text: str, target_words: int = 280):
    paras = [p.strip() for p in text.split("\n")]
    chunks, cur, wcount = [], [], 0
    for p in paras:
        if not p:
            continue
        pw = len(p.split())
        if wcount + pw > target_words and cur:
            chunks.append("\n".join(cur))
            cur, wcount = [p], pw
        else:
            cur.append(p)
            wcount += pw
    if cur:
        chunks.append("\n".join(cur))
    return chunks if chunks else [text]

def safe_truncate(s: str, max_chars: int = 1200) -> str:
    return (s[:max_chars] + "…") if (s and len(s) > max_chars) else s
