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

