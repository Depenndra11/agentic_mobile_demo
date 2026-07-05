from pathlib import Path

from dotenv import load_dotenv

from utils.llm import get_client, generate_content, strip_code_fences
from utils.logger import get_logger

load_dotenv()

logger = get_logger(__name__)


class PageAgent:

    def __init__(self):

        self.client = get_client()

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
    # Load Captured Screen XML
    # ---------------------------------------

    def load_xml(self):
        xml = (
            self.project_root
            / "artifacts"
            / "screen.xml"
        )

        if not xml.exists():
            raise FileNotFoundError(
                f"{xml} not found — run the UI Inspector agent first."
            )

        return xml.read_text(
            encoding="utf-8"
        )

    # ---------------------------------------
    # Generate Page Object
    # ---------------------------------------

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

        text = generate_content(self.client, prompt)

        return strip_code_fences(text)

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

        logger.info("Page object created: %s", output)

    # ---------------------------------------

    def run(self):

        logger.info("Page agent started")

        code = self.generate_page()

        self.save_page(code)

        logger.info("Page agent completed")


if __name__ == "__main__":

    PageAgent().run()