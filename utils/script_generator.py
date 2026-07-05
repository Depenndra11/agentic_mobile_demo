import json

from google import genai

from config.settings import Settings


class ScriptGenerator:

    def __init__(self):

        self.client = genai.Client(
            api_key=Settings.GEMINI_API_KEY
        )

    def generate_script(self, testcase):

        prompt = f"""
        You are a Senior Python Automation Engineer.
        
        Generate ONLY pytest code.
        
        Framework Rules
        
        1. Use pytest
        
        2. Reuse page objects
        
        3. Do not explain
        
        4. Add proper marker
        
        Smoke -> @pytest.mark.smoke
        
        Sanity -> @pytest.mark.sanity
        
        Regression -> @pytest.mark.regression
        
        Test Case
        
        {json.dumps(testcase, indent=2)}
        """

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text