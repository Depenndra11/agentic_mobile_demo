from google import genai
from openai import OpenAI

from config.settings import Settings


class LLMTool:

    def __init__(self):

        self.provider = Settings.LLM_PROVIDER.lower()

        if self.provider == "gemini":
            self.client = genai.Client(
                api_key=Settings.GEMINI_API_KEY
            )

        elif self.provider == "openai":
            self.client = OpenAI(
                api_key=Settings.OPENAI_API_KEY
            )

        else:
            raise ValueError(
                f"Unsupported LLM Provider : {self.provider}"
            )

    def ask(self, prompt: str) -> str:

        if self.provider == "gemini":

            response = self.client.models.generate_content(
                model=Settings.MODEL,
                contents=prompt
            )

            return response.text

        response = self.client.responses.create(
            model=Settings.MODEL,
            input=prompt
        )

        return response.output_text