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

