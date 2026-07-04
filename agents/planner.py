import json

from tools.llm_tool import LLMTool


class PlannerAgent:

    def __init__(self):
        self.llm = LLMTool()

    def plan(self, requirement: str) -> dict:
        prompt = f"""
        You are a Senior Mobile Test Automation Architect.

        Convert the following requirement into a JSON test plan.

        Requirement:
        {requirement}

        Return ONLY valid JSON in this format:

        {{
            "feature": "",
            "preconditions": [],
            "test_steps": [],
            "expected_result": ""
        }}
        """

        response = self.llm.ask(prompt)

        # Remove markdown if Gemini returns ```json ... ```
        response = response.replace("```json", "").replace("```", "").strip()

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "error": "Invalid JSON returned by LLM",
                "raw_response": response
            }