import json
from pathlib import Path

from dotenv import load_dotenv

from utils.llm import get_client, generate_content, strip_code_fences
from utils.excel_reader import ExcelReader
from utils.logger import get_logger

load_dotenv()

logger = get_logger(__name__)


class Executor:

    def __init__(self):

        self.client = get_client()

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

        text = generate_content(self.client, prompt)

        return strip_code_fences(text)

    # -----------------------------------------
    # Save Script
    # -----------------------------------------

    def save_script(self, testcase, code):

        tc_id = testcase.get("ID") or testcase.get("id")

        if not tc_id:
            raise ValueError(f"Test case is missing an ID: {testcase}")

        filename = tc_id.lower().replace(" ", "_")

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

        logger.info("Created: %s", output.name)

    # -----------------------------------------

    def run(self):

        excel = (
            self.project_root
            / "agents"
            / "testcases.xlsx"
        )

        if not excel.exists():
            raise FileNotFoundError(
                f"{excel} not found — run the Planner agent first."
            )

        reader = ExcelReader(excel)

        testcases = reader.get_testcases()

        logger.info("Generating %d script(s)", len(testcases))

        failures = []

        for tc in testcases:
            try:
                code = self.generate_script(tc)
                self.save_script(tc, code)
            except Exception as exc:
                logger.error(
                    "Failed to generate script for %s: %s",
                    tc.get("ID", "<unknown>"), exc
                )
                failures.append(tc.get("ID", "<unknown>"))

        if failures:
            logger.warning(
                "Script generation finished with %d failure(s): %s",
                len(failures), failures
            )
        else:
            logger.info("Script generation completed successfully")


if __name__ == "__main__":

    Executor().run()
