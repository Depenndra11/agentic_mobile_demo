import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # automation_type = web | mobile
    AUTOMATION_TYPE = os.getenv("AUTOMATION_TYPE", "web")

    # Browser
    BROWSER = os.getenv("BROWSER", "chrome")

    # Web URL
    BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com")