from pathlib import Path

from utils.logger import get_logger

logger = get_logger(__name__)


class UIInspector:

    def __init__(self, driver):

        self.driver = driver

    # ----------------------------------------
    # Capture Current Screen XML
    # ----------------------------------------

    def capture_page_source(self):

        xml = self.driver.page_source

        output = (
            Path(__file__).resolve().parent.parent
            / "artifacts"
            / "screen.xml"
        )

        output.parent.mkdir(
            exist_ok=True
        )

        output.write_text(
            xml,
            encoding="utf-8"
        )

        logger.info("Page source saved: %s", output)

        return output


if __name__ == "__main__":

    # Reuse driver from conftest
    from tests.conftest import get_driver

    driver = get_driver()

    try:
        inspector = UIInspector(driver)
        inspector.capture_page_source()
    finally:
        driver.quit()