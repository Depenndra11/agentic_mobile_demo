import json
from pathlib import Path

from dotenv import load_dotenv
from google import genai

from config.settings import Settings
from utils.excel_reader import ExcelReader

load_dotenv()


class Executor:

    def __init__(self):

        self.client = genai.Client(
            api_key=Settings.GEMINI_API_KEY
        )

        self.project_root = Path(__file__).resolve().parent.parent

    # -----------------------------------------
    # Load Prompt
    # -----------------------------------------

    def load_prompt(self):

        prompt_file = (
            self.project_root
            / "prompts"
            / "script_prompt.txt"
        )

        return prompt_file.read_text(
            encoding="utf-8"
        )

    # -----------------------------------------
    # Requirement
    # -----------------------------------------

    def load_requirement(self):

        file = (
            self.project_root
            / "requirements"
            / "login_requirement.txt"
        )

        return file.read_text(
            encoding="utf-8"
        )

    # -----------------------------------------
    # Page Object
    # -----------------------------------------

    def load_page(self):

        page = (
            self.project_root
            / "pages"
            / "login_page.py"
        )

        return page.read_text(
            encoding="utf-8"
        )

    # -----------------------------------------
    # Generate Script
    # -----------------------------------------

    def generate_script(self, testcase):

        prompt = self.load_prompt()

        prompt = prompt.replace(
            "{requirement}",
            self.load_requirement()
        )

        prompt = prompt.replace(
            "{page}",
            self.load_page()
        )

        prompt = prompt.replace(
            "{testcase}",
            json.dumps(testcase, indent=2)
        )

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    # -----------------------------------------
    # Save Script
    # -----------------------------------------

    def save_script(self, testcase, code):

        filename = (
            testcase["ID"]
            .lower()
            .replace(" ", "_")
        )

        output = (
            self.project_root
            / "tests"
            / f"test_{filename}.py"
        )

        output.parent.mkdir(
            exist_ok=True
        )

        output.write_text(
            code,
            encoding="utf-8"
        )

        print(f"✅ Created : {output.name}")

    # -----------------------------------------

    def run(self):

        excel = (
            self.project_root
            / "agents"
            / "testcases.xlsx"
        )

        reader = ExcelReader(excel)

        testcases = reader.get_testcases()

        print(f"\nGenerating {len(testcases)} scripts...\n")

        for tc in testcases:

            code = self.generate_script(tc)

            self.save_script(tc, code)

        print("\n✅ Script Generation Completed")


if __name__ == "__main__":

    Executor().run()