"""
Shared helpers for calling the LLM and cleaning up its responses.

Centralizing this avoids every agent hardcoding the model name and
duplicating retry / response-cleaning logic.
"""

import re

from google import genai
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

from config.settings import Settings


_CODE_FENCE_RE = re.compile(r"^```[a-zA-Z]*\n|\n```$", re.MULTILINE)


def get_client() -> genai.Client:
    """Single place to build the Gemini client from settings."""
    return genai.Client(api_key=Settings.GEMINI_API_KEY)


@retry(
    reraise=True,
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(Exception),
)
def generate_content(client: genai.Client, prompt: str, **config) -> str:
    """
    Call the configured model with basic retry/backoff so a single
    transient API error doesn't kill the whole pipeline.
    """
    response = client.models.generate_content(
        model=Settings.MODEL,
        contents=prompt,
        **({"config": config} if config else {}),
    )
    return response.text


def strip_code_fences(text: str) -> str:
    """
    LLMs frequently wrap code in ```python ... ``` fences even when
    told not to. Writing that straight to a .py file breaks it.
    This strips a single leading/trailing fence if present.
    """
    if text is None:
        return ""

    text = text.strip()

    if text.startswith("```"):
        # Drop the opening fence (with optional language tag)
        text = re.sub(r"^```[a-zA-Z]*\n?", "", text, count=1)

    if text.endswith("```"):
        text = re.sub(r"\n?```$", "", text, count=1)

    return text.strip()
