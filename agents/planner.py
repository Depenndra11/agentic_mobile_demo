
import json
from pathlib import Path

from dotenv import load_dotenv
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

from utils.llm import get_client, generate_content
from utils.logger import get_logger

load_dotenv()

logger = get_logger(__name__)


class Planner:

    def __init__(self):
        self.client = get_client()

    def load_prompt(self):
        prompt_file = (
            Path(__file__).resolve().parent.parent
            / "prompts"
            / "planner_prompt.txt"
        )
        return prompt_file.read_text(encoding="utf-8")

    def generate_test_cases(self):
        prompt = self.load_prompt()

        requirement_file = (
            Path(__file__).resolve().parent.parent
            / "requirements"
            / "login_requirement.txt"
        )

        requirement = requirement_file.read_text(encoding="utf-8")

        prompt = prompt.replace("{requirement}", requirement)

        text = generate_content(
            self.client,
            prompt,
            response_mime_type="application/json",
        )

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            logger.error("Gemini returned non-JSON response:\n%s", text)
            raise

    @staticmethod
    def remove_duplicates(testcases):
        unique = []
        seen = set()

        for tc in testcases:
            scenario = tc.get("scenario", "").strip().lower()
            if scenario not in seen:
                seen.add(scenario)
                unique.append(tc)

        return unique

    @staticmethod
    def assign_ids(testcases):
        for i, tc in enumerate(testcases, start=1):
            tc["id"] = f"TC{i:02d}"
        return testcases

    @staticmethod
    def format_value(value):
        if value is None:
            return ""

        if isinstance(value, list):
            return "\n".join(map(str, value))

        if isinstance(value, dict):
            return json.dumps(value, indent=2)

        return str(value)

    def save_excel(self, testcases):
        wb = Workbook()
        ws = wb.active
        ws.title = "Test Cases"

        headers = [
            "ID",
            "Module",
            "Scenario",
            "Steps",
            "Test Data",
            "Expected Result",
            "Priority",
            "Test Type",
            "Execution Type",
            "Automation Status"
        ]

        ws.append(headers)

        fill = PatternFill(start_color="1F4E78",
                           end_color="1F4E78",
                           fill_type="solid")
        font = Font(bold=True, color="FFFFFF")

        for cell in ws[1]:
            cell.fill = fill
            cell.font = font

        for tc in testcases:
            ws.append([
                tc.get("id", ""),
                tc.get("module", ""),
                tc.get("scenario", ""),
                self.format_value(tc.get("steps")),
                self.format_value(tc.get("test_data")),
                self.format_value(tc.get("expected")),
                tc.get("priority", ""),
                tc.get("test_type", ""),
                tc.get("execution_type", ""),
                tc.get("automation_status", "")
            ])

        for column in ws.columns:
            max_len = max(len(str(c.value)) if c.value else 0 for c in column)
            ws.column_dimensions[column[0].column_letter].width = min(max_len + 5, 50)

        output = Path(__file__).resolve().parent / "testcases.xlsx"
        wb.save(output)

        logger.info("Excel created: %s", output)

    def run(self):
        logger.info("Planner agent started")

        testcases = self.generate_test_cases()

        if not isinstance(testcases, list):
            raise ValueError(
                f"Expected a list of test cases from the LLM, got: {type(testcases)}"
            )

        logger.info("Generated %d test case(s)", len(testcases))

        testcases = self.remove_duplicates(testcases)
        logger.info("%d test case(s) after duplicate removal", len(testcases))

        testcases = self.assign_ids(testcases)

        self.save_excel(testcases)

        logger.info("Planner agent completed")

        return testcases


if __name__ == "__main__":
    Planner().run()
