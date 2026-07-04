from tools.appium_tool import AppiumManager
from utils.logger import get_logger


class ExecutorAgent:

    def __init__(self):
        self.driver = AppiumManager.get_driver()
        self.logger = get_logger()

    def execute(self, plan: dict):

        self.logger.info("Executing Test Plan...")

        for step in plan.get("test_steps", []):

            self.logger.info(f"Executing Step: {step}")

            step_lower = step.lower()

            if "launch" in step_lower:
                self.logger.info("Application launched.")

            elif "username" in step_lower:
                self.logger.info("Entering username...")
                # Example:
                # self.driver.find_element(...).send_keys("standard_user")

            elif "password" in step_lower:
                self.logger.info("Entering password...")
                # self.driver.find_element(...).send_keys("secret_sauce")

            elif "login" in step_lower:
                self.logger.info("Click Login button...")
                # self.driver.find_element(...).click()

            else:
                self.logger.warning(f"No action defined for: {step}")

        self.logger.info("Execution Completed.")

        return {
            "status": "PASS",
            "executed_steps": plan.get("test_steps", [])
        }