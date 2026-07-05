from pathlib import Path

from dotenv import load_dotenv
from google import genai

from config.settings import Settings

load_dotenv()


class PageAgent:

    def __init__(self):

        self.client = genai.Client(
            api_key=Settings.GEMINI_API_KEY
        )

        self.project_root = Path(__file__).resolve().parent.parent

    # ---------------------------------------
    # Load Requirement
    # ---------------------------------------

    def load_requirement(self):

        requirement = (
            self.project_root
            / "requirements"
            / "login_requirement.txt"
        )

        return requirement.read_text(
            encoding="utf-8"
        )




    # ---------------------------------------
    # Load Prompt
    # ---------------------------------------

    def load_prompt(self):

        prompt = (
            self.project_root
            / "prompts"
            / "page_prompt.txt"
        )

        return prompt.read_text(
            encoding="utf-8"
        )

    # ---------------------------------------
    # Generate Page Object
    # ---------------------------------------
    def load_xml(self):
        xml = (
                self.project_root
                / "artifacts"
                / "screen.xml"
        )

        return xml.read_text(
            encoding="utf-8"
        )
    def generate_page(self):

        prompt = self.load_prompt()

        prompt = prompt.replace(
            "{requirement}",
            self.load_requirement()
        )

        prompt = prompt.replace(
            "{xml}",
            self.load_xml()
        )

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    # ---------------------------------------
    # Save File
    # ---------------------------------------

    def save_page(self, code):

        output = (
            self.project_root
            / "pages"
            / "login_page.py"
        )

        output.parent.mkdir(
            exist_ok=True
        )

        output.write_text(
            code,
            encoding="utf-8"
        )

        print(f"\n✅ Page Object Created\n{output}")

    # ---------------------------------------

    def run(self):

        print("=" * 60)
        print("Page Agent Started")
        print("=" * 60)

        code = self.generate_page()

        self.save_page(code)

        print("\n✅ Page Object Generated")


if __name__ == "__main__":

    PageAgent().run()