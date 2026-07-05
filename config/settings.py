import json
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class Settings:

    CONFIG_PATH = Path(__file__).parent / "config.json"

    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        CONFIG = json.load(file)

    WEB = CONFIG["web"]

    DEVICE = WEB["device"]
    BASE_URL = WEB["base_url"]
    USERNAME = WEB["username"]
    PASSWORD = WEB["password"]

    LLM = CONFIG["llm"]

    MODEL = LLM["model"]

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")