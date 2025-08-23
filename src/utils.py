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
