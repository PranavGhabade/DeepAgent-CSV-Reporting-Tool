"""
LLM Configuration

Initializes an OpenAI-compatible LLM client.

Although this file is named gemini.py for backward compatibility,
it can connect to any OpenAI-compatible endpoint by reading the
configuration from the .env file.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")

if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY not found in .env"
    )

if not OPENAI_BASE_URL:
    raise ValueError(
        "OPENAI_BASE_URL not found in .env"
    )

if not OPENAI_MODEL:
    raise ValueError(
        "OPENAI_MODEL not found in .env"
    )

llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
    model=OPENAI_MODEL,
    temperature=0,
    max_retries=3,
    timeout=120,
)