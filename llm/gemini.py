

"""
LLM Configuration

Initializes the OpenAI-compatible LLM
for use across all agents.
"""

import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")

if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY not found. Please add it to your .env file."
    )

if not OPENAI_BASE_URL:
    raise ValueError(
        "OPENAI_BASE_URL not found. Please add it to your .env file."
    )

if not OPENAI_MODEL:
    raise ValueError(
        "OPENAI_MODEL not found. Please add it to your .env file."
    )

llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
    model=OPENAI_MODEL,
    temperature=0,
    streaming=False,
    max_tokens=16384,
)




# """
# Gemini LLM Configuration

# Initializes the Gemini model for use across all agents.
# """

# import os

# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI

# load_dotenv()

# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# if not GEMINI_API_KEY:
#     raise ValueError(
#         "GEMINI_API_KEY not found. Please add it to your .env file."
#     )

# llm = ChatGoogleGenerativeAI(
#     model=os.getenv("GEMINI_MODEL"),
#     google_api_key=GEMINI_API_KEY,
#     temperature=0,
# )